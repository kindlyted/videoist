from app import create_app
from models import db, Video, User

def fix_video_user_ids():
    """修复视频记录中的user_id字段，将用户名字符串替换为用户ID数值"""
    app = create_app()
    
    with app.app_context():
        # 查找用户名为admin的用户
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            print('未找到用户名为admin的用户')
            return
        
        # 查找所有user_id为'admin'字符串的视频记录
        videos_to_fix = Video.query.filter(Video.user_id == 'admin').all()
        
        print(f'找到{len(videos_to_fix)}条需要修复的视频记录')
        
        # 更新每条视频记录的user_id字段
        for video in videos_to_fix:
            print(f'修复视频记录ID {video.id}: 将user_id从"{video.user_id}"更新为{admin_user.id}')
            video.user_id = admin_user.id
        
        # 提交更改到数据库
        db.session.commit()
        print('所有视频记录修复完成')

if __name__ == '__main__':
    fix_video_user_ids()