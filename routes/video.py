# routes/video.py
import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from functools import wraps
from flask import Blueprint, request, jsonify, url_for, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import Config
from models import db, Video, WordPressSite, WechatAccount, User
from services.video.cookies_core import (
    check_cookies_validity,
    get_platform_cookies,
    get_cookies_with_playwright,
    PLATFORM_LOGIN_URLS
)

from services.common.prompt_renderer import PromptRenderer
from services.video.video_core import (
    speaking,
    process_dialogue,
    merge_subtitles,
    create_video_multi,
    create_video_single,  # Linux
    creating_cover,
    extractting,
    basic_auth_token,
    process_markdown_images,
    posting,
    markdown_to_html,
    convert_webp_to_jpg
)
from services.common.utils import generating_byds, generating_jskb
from services.video.post_video import dy_video_upload, sph_video_upload, xhs_video_upload
from services.video.publisher_core import WeChatPublisher
from services.video.db_utils import get_db_credentials
from services.common.error_codes import ErrorCode
from services.common.utils import get_error_message, create_error_response, create_success_response

# 创建蓝图
video_bp = Blueprint('video', __name__)

# 异步路由处理装饰器
def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return current_app.ensure_sync(f)(*args, **kwargs)
    return wrapped

# --------------------------
# 视频创作子系统
# --------------------------

@video_bp.route('/count-characters', methods=['POST'])
def count_characters():
    data = request.get_json()
    text = data.get('text', '')
    return jsonify({'count': len(text)})

@video_bp.route('/voice-options', methods=['GET'])
def get_voice_options():
    """为前端提供音色选择列表"""
    return jsonify({
        'voice_names': Config.VOICE_NAMES,
        'default_voice': Config.DEFAULT_VOICE
    })

@video_bp.route('/platform-stats', methods=['GET'])
@jwt_required()
def get_platform_stats():
    """获取平台统计数据（WordPress站点数量和微信公众号数量）"""""
    try:
        # 获取当前用户名
        current_username = get_jwt_identity()
        
        # 根据用户名查询用户ID
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify(create_error_response(ErrorCode.USER_NOT_FOUND)), 404
        
        # 使用用户ID查询WordPress站点和微信公众号数量
        wordpress_count = WordPressSite.query.filter_by(user_id=user.id, is_active=True).count()
        
        # 获取当前用户微信公众号数量
        wechat_count = WechatAccount.query.filter_by(user_id=user.id, is_active=True).count()

        
        return jsonify({
            'wordpress_sites_count': wordpress_count,
            'wechat_accounts_count': wechat_count
        })
    except Exception as e:
        return jsonify({'error': f'获取平台统计数据时出错: {str(e)}'}), 500

@video_bp.route('/generate-title', methods=['POST'])
def generate_title():
    data = request.get_json()
    input_text = data.get('text', '')
    if not input_text:
        return jsonify(create_error_response(ErrorCode.INPUT_TEXT_MISSING)), 400
    
    try:
        title_txt = generating_byds(input_text, str(Config.PROMPT_DIR / "top_title.prompt"))[:12]
        cover_txt = generating_byds(input_text, str(Config.PROMPT_DIR / "cover_title.prompt"))
        
        return jsonify({
            'title': title_txt,
            'cover': cover_txt
        })
    except Exception as e:
        return jsonify(create_error_response(ErrorCode.TITLE_GENERATION_ERROR, str(e))), 500

@video_bp.route('/post-article', methods=['POST'])
@jwt_required()
def post_article():
    # 只处理JSON格式的请求
    data = request.get_json()
    url = data.get('url')
    mode = data.get('mode', '朗诵')
    wordpress_switch = data.get('wordpress_switch', 'off')
    wechat_switch = data.get('wechat_switch', 'off')
    

    try:
        # 提取内容
        # 更全面的URL验证
        if not url:
            return jsonify(create_error_response(ErrorCode.URL_MISSING)), 400
        
        if not (url.startswith("http://") or url.startswith("https://")):
            content_text = url
        else:
            # 验证URL格式
            try:
                from urllib.parse import urlparse
                parsed_url = urlparse(url)
                if not parsed_url.netloc:
                    content_text = url
                else:
                    content_text = extractting(url)
            except Exception:
                content_text = url
        
        if not content_text:
            return jsonify(create_error_response(ErrorCode.FILE_PROCESSING_ERROR)), 400
        
        # 生成结构化内容
        results = {}
        renderer = PromptRenderer()

        # Step1: 内容分析
        analysis_result = generating_jskb(
            content=content_text,
            # prompt_path=Config.PROMPT_DIR / 'content_analysis.prompt'
            prompt_path=Config.PROMPT_DIR / 'html_classify.prompt'
        )
        results['analysis'] = json.loads(analysis_result)

        # Step2: 内容改写
        prompt_vars = {
            "article_type": results['analysis']['type'],
            # 未来扩展点：可随时添加新变量
            "min_length": 800,
            "image_count": 2
        }
        
        # 渲染并保存临时提示词
        renderer.render_to_file(
            template_dir=Config.PROMPT_DIR,
            template_name='rewrite_content',
            context=prompt_vars,
            output_path=Config.PROMPT_DIR / 'tmp.prompt'
        )

        rewrite_result = generating_jskb(
            content=content_text,
            prompt_path=Config.PROMPT_DIR / 'tmp.prompt'
        )
        material = json.loads(rewrite_result)

        
        # 生成音频脚本
        prompt_file = "broadcastscript.prompt" if mode == "对话" else "audioscript.prompt"
        audioscript = generating_byds(material["content"], str(Config.PROMPT_DIR / prompt_file)) 
        
        # 从数据库获取凭据
        wp_creds = get_db_credentials('wordpress')
        wechat_creds = get_db_credentials('wechat')
        
        # 调试信息
        # print(f"wp_creds type: {type(wp_creds)}, value: {wp_creds}")
        # print(f"wechat_creds type: {type(wechat_creds)}, value: {wechat_creds}")
        
        # 检查凭据完整性
        wp_creds_valid = all([wp_creds.get('url'), wp_creds.get('username'), wp_creds.get('password')])
        wechat_creds_valid = all([wechat_creds.get('app_id'), wechat_creds.get('app_secret')])
        
        # 如果凭据不完整，强制关闭对应功能开关
        if not wp_creds_valid:
            wordpress_switch = 'off'  # 强制关闭WordPress发布功能
        if not wechat_creds_valid:
            wechat_switch = 'off'      # 强制关闭微信公众号发布功能
        
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
        
        # 从数据库获取标签映射

        tag_site = WordPressSite.query.filter_by(is_active=True).first()
        # 确保tag_index是字典格式
        if tag_site and tag_site.wp_tag:
            # 如果wp_tag是字符串，尝试解析为JSON
            if isinstance(tag_site.wp_tag, str):
                try:
                    tag_index = json.loads(tag_site.wp_tag)
                except json.JSONDecodeError:
                    # 如果解析失败，使用默认值
                    tag_index = {"国际教育": 7}
            else:
                # 如果已经是字典格式，直接使用
                tag_index = tag_site.wp_tag
        else:
            # 如果没有找到或为空，使用默认值
            tag_index = {"国际教育": 7}
        # print(tag_index)

        # 从数据库获取SEO页脚
        seo_footer_site = WordPressSite.query.filter_by(is_active=True).first()
        SEO_FOOTER = seo_footer_site.wp_footer if seo_footer_site and seo_footer_site.wp_footer else ""
        
        # Step3: 添加标签
        prompt_vars = {
            "prefix_options": tag_index["prefix"],
            "categories_options": list(tag_index["categories"].keys()),
            "tags_options": list(tag_index["tags"].keys()),
            # 未来扩展点：可随时添加新变量
            "min_length": 800,
            "image_count": 2
        }
        # 渲染并保存临时提示词
        renderer.render_to_file(
            template_dir=Config.PROMPT_DIR,
            template_name='rewrite_tags',
            context=prompt_vars,
            output_path=Config.PROMPT_DIR / 'tmp.prompt'
        )
        tag_result = generating_jskb(
            content=content_text,
            prompt_path=Config.PROMPT_DIR / 'tmp.prompt'
        )
        material.update(json.loads(tag_result))
        
        # Step4: 图像提示词生成
        image_prompt_content = material["content"]
        image_result = generating_jskb(
            content=image_prompt_content,
            prompt_path=Config.PROMPT_DIR / 'image_generation.prompt'
        )
        results['images'] = json.loads(image_result)

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
        wp_payload["categories"] = [tag_index["categories"].get(material["categories"], 2)]
        wp_payload["tags"] = [tag_index["tags"][item] for item in material["tags"] if item in tag_index["tags"]]
        
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
        return jsonify(create_error_response(ErrorCode.FILE_PROCESSING_ERROR, str(e))), 500
    
    wx_result_msg = ""
    if wx_result:
        wx_result_msg = get_error_message(ErrorCode.WECHAT_PUBLISH_SUCCESS)
    elif wx_result is None:
        wx_result_msg = get_error_message(ErrorCode.WECHAT_PUBLISH_SKIPPED)
    else:
        wx_result_msg = get_error_message(ErrorCode.WECHAT_PUBLISH_FAILED)
    
    return jsonify({
        'website_url': post["link"] if post else get_error_message(ErrorCode.WORDPRESS_PUBLISH_SKIPPED),
        'article_text': audioscript,
        'working_dir': working_dir,
        'wx_result': wx_result_msg
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
    "傣momo": "zh-CN-YunyangNeural",
    "喇cici": "zh-CN-XiaoxiaoNeural"
    }
    if not cover_txt:
        return jsonify(create_error_response(ErrorCode.COVER_DESCRIPTION_MISSING)), 400
    
    if not input_text:
        return jsonify(create_error_response(ErrorCode.INPUT_TEXT_MISSING)), 400
    
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
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify(create_error_response(ErrorCode.USER_NOT_FOUND)), 404
        
        video = Video(
            title=title_txt,
            description=input_text[:200],  # 取前200个字符作为描述
            file_path=url_for('storage_files', filename=f'output/outputs/{base_filename}.mp4'),
            thumbnail_path=url_for('storage_files', filename=f'output/outputs/{base_filename}.png'),
            user_id=user.id
        )
        db.session.add(video)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': get_error_message(ErrorCode.VIDEO_GENERATION_SUCCESS),
            'cover_path': url_for('storage_files', filename=f'output/outputs/{base_filename}.png'),
            'video_path': url_for('storage_files', filename=f'output/outputs/{base_filename}.mp4')
        })
    except Exception as e:
        error_message = f'{get_error_message(ErrorCode.VIDEO_GENERATION_ERROR)}: {str(e)}'
        return jsonify({
            'success': False,
            'message': error_message
        }), 500

# 获取用户视频列表
@video_bp.route('/videos', methods=['GET'])
@jwt_required()
def get_videos():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    videos = Video.query.filter_by(user_id=user.id).order_by(Video.created_at.desc()).all()

    videos_data = []
    for video in videos:
        videos_data.append({
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'file_path': video.file_path,
            'thumbnail_path': video.thumbnail_path,
            'created_at': video.created_at.isoformat()
        })
    
    # 返回结构化的响应
    return jsonify({
        'success': True,
        'data': videos_data
    })

@video_bp.route('/video/<int:video_id>', methods=['GET'])
@jwt_required()
def get_video_detail(video_id):
    """获取指定视频的详细信息"""
    # 获取当前用户
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify(create_error_response(ErrorCode.USER_NOT_LOGGED_IN)), 401
        
    # 获取视频信息
    video = Video.query.get_or_404(video_id)
    
    # 检查视频是否属于当前用户
    if video.user_id != user.id:
        return jsonify(create_error_response(ErrorCode.VIDEO_ACCESS_DENIED)), 403
    
    # 返回视频详细信息
    return jsonify({
        'success': True,
        'data': {
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'file_path': video.file_path,
            'thumbnail_path': video.thumbnail_path,
            'created_at': video.created_at.isoformat(),
            'user_id': video.user_id
        }
    })

@video_bp.route('/video/<int:video_id>', methods=['DELETE'])
@jwt_required()
def delete_video(video_id):
    """删除指定视频"""
    # 获取当前用户
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify(create_error_response(ErrorCode.USER_NOT_LOGGED_IN)), 401
        
    # 获取视频信息
    video = Video.query.get_or_404(video_id)
    
    # 检查视频是否属于当前用户
    if video.user_id != user.id:
        return jsonify(create_error_response(ErrorCode.VIDEO_DELETE_DENIED)), 403
    
    # 删除视频
    db.session.delete(video)
    db.session.commit()
    
    return jsonify(create_success_response(ErrorCode.VIDEO_DELETION_SUCCESS))

@video_bp.route('/video-stats', methods=['GET'])
@jwt_required()
def get_video_stats():
    """获取视频统计数据（视频总数）"""
    try:
        # 获取当前用户名
        current_username = get_jwt_identity()
        
        # 根据用户名查询用户ID
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify(create_error_response(ErrorCode.USER_NOT_FOUND)), 404
        
        # 使用用户ID查询视频数量
        video_count = Video.query.filter_by(user_id=user.id).count()
        
        return jsonify({
            'video_count': video_count
        })
    except Exception as e:
        error_message = f'{get_error_message(ErrorCode.VIDEO_STATS_ERROR)}: {str(e)}'
        return jsonify({'error': error_message}), 500

# 视频发布
@video_bp.route('/publish-video', methods=['POST'])
@jwt_required()
def publish_video():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify(create_error_response(ErrorCode.USER_NOT_LOGGED_IN)), 401

    data = request.get_json()
    video_url = data.get('video_path', '')
    cover_url = data.get('cover_path', '')
    base_filename = video_url.split('/')[-1].split('.')[0]
    # 转换为磁盘路径
    video_path = Path(Config.OUTPUT_DIR) / f'{base_filename}.mp4'
    cover_path = Path(Config.OUTPUT_DIR) / f'{base_filename}.png' 
    title = data.get('title', '')
    desc = data.get('desc', '')
    
    # from services.video.cookies_core import check_cookies_validity, get_platform_cookies
    
    # 检查所有平台的cookies是否有效
    platforms_status = {
        'xiaohongshu': check_cookies_validity(user.id, 'xiaohongshu'),
        'douyin': check_cookies_validity(user.id, 'douyin'),
        'shipinhao': check_cookies_validity(user.id, 'shipinhao')
    }
    
    # 如果有任何平台的cookies无效，返回需要登录的平台列表
    invalid_platforms = [p for p, valid in platforms_status.items() if not valid]
    if invalid_platforms:
        return jsonify({
            'error': get_error_message(ErrorCode.COOKIES_INVALID),
            'invalid_platforms': invalid_platforms,
            'message': get_error_message(ErrorCode.PLATFORM_LOGIN_REQUIRED)
        }), 403
    
    try:
        results = {}
        
        # 上传小红书
        xhs_cookies = get_platform_cookies(user.id, 'xiaohongshu')
        results['xiaohongshu'] = xhs_video_upload(video_path, cover_path, title, desc, cookies_data=xhs_cookies)
        
        # 上传抖音
        dy_cookies = get_platform_cookies(user.id, 'douyin')
        results['douyin'] = dy_video_upload(video_path, cover_path, title, desc, cookies_data=dy_cookies)
        
        # 上传视频号
        sph_cookies = get_platform_cookies(user.id, 'shipinhao')
        results['shipinhao'] = sph_video_upload(video_path, cover_path, title, desc, cookies_data=sph_cookies)
        
        # 检查上传结果
        success = all(results.values())
        if success:
            return jsonify(create_success_response(ErrorCode.VIDEO_PUBLISH_SUCCESS))
        else:
            failed_platforms = [p for p, r in results.items() if not r]
            return jsonify({
                'error': get_error_message(ErrorCode.VIDEO_PUBLISH_PARTIAL_FAILURE),
                'failed_platforms': failed_platforms
            }), 500
            
    except Exception as e:
        error_message = f'{get_error_message(ErrorCode.VIDEO_PUBLISH_ERROR)}: {str(e)}'
        return jsonify({'error': error_message}), 500

# --------------------------
# 平台 Cookie 管理 API
# --------------------------

@video_bp.route('/platform-login-status', methods=['GET'])
@jwt_required()
def get_platform_login_status():
    """获取所有平台的登录状态"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify(create_error_response(ErrorCode.USER_NOT_LOGGED_IN)), 401
    
    # from services.video.cookies_core import check_cookies_validity
    
    platforms_status = {
        'xiaohongshu': check_cookies_validity(user.id, 'xiaohongshu'),
        'douyin': check_cookies_validity(user.id, 'douyin'),
        'shipinhao': check_cookies_validity(user.id, 'shipinhao')
    }
    
    return jsonify(platforms_status)

@video_bp.route('/platform-login', methods=['POST'])
@jwt_required()
def platform_login():
    """启动平台登录流程"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify(create_error_response(ErrorCode.USER_NOT_LOGGED_IN)), 401
    
    data = request.get_json()
    platform = data.get('platform')
    if not platform:
        return jsonify(create_error_response(ErrorCode.PLATFORM_NOT_SPECIFIED)), 400
        
    # from services.video.cookies_core import PLATFORM_LOGIN_URLS, get_cookies_with_playwright
    
    if platform not in PLATFORM_LOGIN_URLS:
        return jsonify(create_error_response(ErrorCode.INVALID_PLATFORM)), 400
    
    try:
        # 在同步函数中运行异步操作
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            get_cookies_with_playwright(
                url=PLATFORM_LOGIN_URLS[platform],
                platform_name=platform,
                user_id=user.id
            )
        )
        loop.close()
        
        if result['success']:
            return jsonify({'success': True, 'message': get_error_message(ErrorCode.LOGIN_SUCCESS)})
        else:
            return jsonify({'success': False, 'error': result['message']}), 500
            
    except Exception as e:
        error_message = f'{get_error_message(ErrorCode.LOGIN_ERROR)}: {str(e)}'
        return jsonify({'success': False, 'error': error_message}), 500
