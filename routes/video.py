# routes/video.py

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from flask import Blueprint, request, jsonify, send_file, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config

# 创建蓝图
video_bp = Blueprint('video', __name__)
from services.video.video_core import (
    speaking,
    process_dialogue,
    merge_subtitles,
    create_video_multi,
    create_video_single,  # Linux
    creating_cover,
    generating_byds,
    extractting,
    basic_auth_token,
    generating_jskb,
    process_markdown_images,
    posting,
    markdown_to_html,
    convert_webp_to_jpg
)
from services.video.post_video import dy_video_upload, sph_video_upload, xhs_video_upload
from services.video.publisher_core import WeChatPublisher
from services.video.db_utils import get_db_credentials

# --------------------------
# 视频创作子系统
# --------------------------

@video_bp.route('/count-characters', methods=['POST'])
def count_characters():
    data = request.get_json()
    text = data.get('text', '')
    return jsonify({'count': len(text)})

@video_bp.route('/generate-title', methods=['POST'])
def generate_title():
    data = request.get_json()
    input_text = data.get('text', '')
    if not input_text:
        return jsonify({'error': '请输入台词'}), 400
    
    try:
        title_txt = generating_byds(input_text, str(Config.PROMPT_DIR / "top_title.prompt"))[:12]
        cover_txt = generating_byds(input_text, str(Config.PROMPT_DIR / "cover_title.prompt"))
        
        return jsonify({
            'title': title_txt,
            'cover': cover_txt
        })
    except Exception as e:
        return jsonify({'error': f'生成标题时出错: {str(e)}'}), 500

@video_bp.route('/post-article', methods=['POST'])
@jwt_required()
def post_article():
    # 只处理JSON格式的请求
    data = request.get_json()
    url = data.get('url')
    mode = data.get('mode', '朗诵')
    wordpress_switch = data.get('wordpress_switch', 'off')
    wechat_switch = data.get('wechat_switch', 'off')
    

    # 更全面的URL验证
    if not url:
        return jsonify({'error': 'URL不能为空'}), 400
    
    if not (url.startswith("http://") or url.startswith("https://")):
        return jsonify({'error': '无效的URL'}), 400
    
    # 验证URL格式
    try:
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        if not parsed_url.netloc:
            return jsonify({'error': '无效的URL格式'}), 400
    except Exception:
        return jsonify({'error': '无效的URL格式'}), 400
    
    try:
        # 提取内容
        content_text = extractting(url)
        if not content_text:
            return jsonify({'error': '内容为空'}), 400

        # 生成结构化内容
        material = json.loads(generating_jskb(content_text, str(Config.PROMPT_DIR / "structure.prompt")))
        
        # 生成音频脚本
        prompt_file = "broadcastscript.prompt" if mode == "对话" else "audioscript.prompt"
        audioscript = generating_byds(material["content"], str(Config.PROMPT_DIR / prompt_file)) #material["content"]和process_markdown_images中的content不同
    
        # 从数据库获取凭据
        wp_creds = get_db_credentials('wordpress')
        wechat_creds = get_db_credentials('wechat')
        
        # 检查凭据完整性
        wp_creds_valid = all([wp_creds.get('url'), wp_creds.get('username'), wp_creds.get('password')])
        wechat_creds_valid = all([wechat_creds.get('app_id'), wechat_creds.get('app_secret')])
        
        # 如果凭据为空，强制关闭对应功能
        # if not wp_creds_valid:
        #     wordpress_switch = 'off'
        # if not wechat_creds_valid:
        #     wechat_switch = 'off'
        if wordpress_switch != 'on' and wechat_switch != 'on':
        
            return jsonify({
                'website_url': 'WordPress发布已跳过',
                'article_text': audioscript,
                'working_dir': '图片处理已跳过',
                'wx_result': '公众号发布已跳过'
            })

        # 生成基准文件名（当前日期时间）
        working_dir = datetime.now().strftime("%Y%m%d%H%M%S")
        # 使用配置的工作目录路径
        working_path = Config.ARTICLE_DIR / working_dir
        working_path.mkdir(parents=True, exist_ok=True)  # 自动创建目录
        
        # WordPress配置 - 从数据库获取
        WORDPRESS_URL = wp_creds.get('url', '')
        USERNAME = wp_creds.get('username', '')
        APPLICATION_PASSWORD = wp_creds.get('password', '')
        
        # 标签映射
        tag_index = {
            "国际教育": 7,
            "定居指南": 49,
            "移民资讯": 8,
            "楼市新闻": 2,
            "房产": 46,
            "教育": 47,
            "海外": 45,
            "留学": 64,
            "移民": 48
        }
        
        token = basic_auth_token(USERNAME, APPLICATION_PASSWORD)
        
        # 初始化文章数据
        wp_payload = {
            "title": "",
            "content": "",
            "status": "publish",
            "featured_media": "",
            "categories": [],
            "tags": []
        }
        
        # 读取HTML文件
        with open(Config.HTML_DIR / "seo_footer_wx.html", "r", encoding="utf-8") as f:
            SEO_FOOTER = f.read()
        
        # 保存material到JSON文件
        with open(Config.ARTICLE_DIR / f"{working_dir}/{working_dir}.json", "w", encoding="utf-8") as f:
            json.dump(material, f, ensure_ascii=False, indent=2)
        
        # 处理Markdown中的所有图片
        processed_content, image_info = process_markdown_images(
            material["content"], 
            WORDPRESS_URL, 
            token, 
            working_dir
        )  
        
        # 设置特色图片(第一张图片或默认)
        if image_info:
            first_image = next(iter(image_info.values()))
            wp_payload["featured_media"] = first_image["id"]
        
        # 设置文章内容
        wp_payload["title"] = material["prefix"] + "|" + material["title"]
        html_content, metadata = markdown_to_html(processed_content)
        wp_payload["content"] = html_content + SEO_FOOTER
        
        # 设置分类和标签
        wp_payload["categories"] = tag_index.get(material["categories"], 2)
        wp_payload["tags"] = [tag_index[item] for item in material["tags"] if item in tag_index]
        
        # 发布文章到WordPress
        post = None
        if wordpress_switch == 'on':
            post = posting(WORDPRESS_URL, token, wp_payload)
    
        # 自动上传到微信公众号
        wx_result = None
        if wechat_switch == 'on':
            convert_webp_to_jpg(Config.ARTICLE_DIR / f"{working_dir}")
            material["content"] = material["content"].replace(".webp)", ".jpg)")
            
            with open(Config.ARTICLE_DIR / f"{working_dir}/{working_dir}.md", "w", encoding="utf-8") as f:
                f.write(material["content"])
            
            publisher = WeChatPublisher(
                app_id=wechat_creds.get('app_id', ''),
                app_secret=wechat_creds.get('app_secret', ''),
                article_name=working_dir,
                source_url=post["link"] if post else ""
            )
            
            wx_result = publisher.publish()
    except Exception as e:
        return jsonify({'error': f'处理URL时出错: {str(e)}'}), 500
    
    return jsonify({
        'website_url': post["link"] if post else "WordPress发布已跳过",
        'article_text': audioscript,
        'working_dir': working_dir,
        'wx_result': "公众号发布成功" if wx_result else ("公众号发布已跳过" if wx_result is None else "公众号发布失败")
    })

@video_bp.route('/generate-video', methods=['POST'])
@jwt_required()
def generate_video():
    # 接收JSON格式的请求
    data = request.get_json()
    input_text = data.get('text', '')
    title_txt = data.get('title', '')
    cover_txt = data.get('cover', '')
    voice = data.get('voice', Config.VOICE_NAMES[4])
    VOICE_MAPPING = {
    "傣momo": "zh-CN-YunxiNeural",
    "喇cici": "zh-CN-XiaoxiaoNeural"
    }
    if not cover_txt:
        return jsonify({'error': '请补充封面描述'}), 400
    
    try:
        # 获取当前日期
        base_filename = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # 文件路径
        txt_file = str(Config.TEXT_DIR / f"{base_filename}.txt")
        srt_file = str(Config.OUTPUT_DIR / f"{base_filename}.srt") 
        audio_filename = str(Config.OUTPUT_DIR / f"{base_filename}.mp3")
        output_filename = str(Config.OUTPUT_DIR / f"{base_filename}.mp4")
        cover_filename = str(Config.OUTPUT_DIR / f"{base_filename}.png")

        # 将输入文本写入文件
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(input_text)
        
        if not os.path.exists(audio_filename) or not os.path.exists(srt_file):
            # 判断是否为对话文本（包含角色前缀）
            is_dialogue = any(
                line.strip().split(':', 1)[0].strip() in VOICE_MAPPING  # 直接检查是否在VOICE_MAPPING的键中
                for line in input_text.split('\n')
                if ':' in line
            )
            
            if is_dialogue:
                asyncio.run(process_dialogue(txt_file, audio_filename, srt_file, VOICE_MAPPING, temp_dir="tmp", silence_duration_ms=500))
            else:
                # 普通单文本处理模式（原基础函数）
                asyncio.run(speaking(audio_filename, srt_file, input_text, voice))
        merge_subtitles(srt_file, 2)
            
        # 生成封面图片
        cover_keywords = generating_byds(cover_txt, str(Path(Config.PROMPT_DIR) / 'cover_keywords.prompt'))
        creating_cover(cover_txt, cover_keywords, cover_filename)
        
        # 根据操作系统选择不同的视频创建函数
        if os.name == 'nt':  # Windows系统
            create_video_multi(srt_file, audio_filename, output_filename, Config.SCREEN_SIZE, title_txt)
        else:  
            create_video_single(srt_file, audio_filename, output_filename, Config.SCREEN_SIZE, title_txt)
        
        # 保存视频记录到数据库
        # current_user_id = get_jwt_identity()
        # video = Video(
        #     title=title_txt,
        #     description=input_text[:200],  # 取前200个字符作为描述
        #     file_path=f'/video/static/output/outputs/{base_filename}.mp4',
        #     thumbnail_path=f'/video/static/output/outputs/{base_filename}.png',
        #     author_id=current_user_id
        # )
        # db.session.add(video)
        # db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '视频生成成功',
            'cover_path': url_for('storage_files', filename=f'output/outputs/{base_filename}.png'),
            'video_path': url_for('storage_files', filename=f'output/outputs/{base_filename}.mp4')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'生成视频时出错: {str(e)}'
        }), 500

@video_bp.route('/publish-video', methods=['POST'])
def publish_video():
    data = request.get_json()
    video_url = data.get('video_path', '')
    print(f"Received video URL: {video_url}")
    cover_url = data.get('cover_path', '')
    base_filename = video_url.split('/')[-1].split('.')[0]
    # 转换为磁盘路径
    video_path = Path(Config.OUTPUT_DIR) / f'{base_filename}.mp4'
    cover_path = Path(Config.OUTPUT_DIR) / f'{base_filename}.png' 
    title = data.get('title', '')
    desc = data.get('desc', '')
    
    try:
        # 上传小红书 
        acct_info = Path(Config.MAIN_STATIC_FOLDER) / 'cookies' / 'cookie_xhs_zhi.json'
        xhs_result = xhs_video_upload(video_path, cover_path, title, desc, acct_info)
        
        # 上传抖音
        acct_info = Path(Config.MAIN_STATIC_FOLDER) / 'cookies' / 'cookie_douyin_zhi.json'
        dy_result = dy_video_upload(video_path, cover_path, title, desc, acct_info)
        
        # 上传视频号
        acct_info = Path(Config.MAIN_STATIC_FOLDER) / 'cookies' / 'cookie_sph_zhi.json'
        sph_result = sph_video_upload(video_path, cover_path, title, desc, acct_info)
        
        if xhs_result and dy_result and sph_result:  # 可根据实际需求调整判断逻辑
            return jsonify({'message': '视频已成功上传到各平台'})
        else:
            return jsonify({'error': '部分平台上传失败'}), 500
    except Exception as e:
        return jsonify({'error': f'上传视频时出错: {str(e)}'}), 500

# @video_bp.route('/download-video')
# @jwt_required()
# def download_video():
#     filename = request.args.get('filename', '')
#     if not filename:
#         return jsonify({'error': '文件名不能为空'}), 400
    
#     file_path = str(Config.OUTPUT_DIR / filename)
#     if not os.path.exists(file_path):
#         return jsonify({'error': '文件不存在'}), 404
    
#     try:
#         return send_file(
#             file_path,
#             as_attachment=True,
#             download_name=f"video_{datetime.now().strftime('%Y%m%d')}.mp4"
#         )
#     except Exception as e:
#         return jsonify({'error': f'下载失败: {str(e)}'}), 500

@video_bp.route('/videos', methods=['GET'])
@jwt_required()
def get_videos():
    from models import Video
    videos = Video.query.all()
    return jsonify([{
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'file_path': video.file_path,
        'thumbnail_path': video.thumbnail_path,
        'created_at': video.created_at.isoformat()
    } for video in videos])

@video_bp.route('/video/<int:video_id>', methods=['GET'])
@jwt_required()
def get_video_detail(video_id):
    from models import Video
    video = Video.query.get_or_404(video_id)
    return jsonify({
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'file_path': video.file_path,
        'thumbnail_path': video.thumbnail_path,
        'created_at': video.created_at.isoformat()
    })

@video_bp.route('/video/<int:video_id>', methods=['DELETE'])
@jwt_required()
def delete_video(video_id):
    from models import Video
    from extensions import db
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return jsonify({'message': '视频删除成功'})

@video_bp.route('/voice-options', methods=['GET'])
def get_voice_options():
    """为前端提供音色选择列表"""
    return jsonify({
        'voice_names': Config.VOICE_NAMES,
        'default_voice': Config.DEFAULT_VOICE
    })

