#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import app, db
from models import User

def delete_users(user_ids):
    """删除指定ID的用户"""
    with app.app_context():
        for user_id in user_ids:
            user = User.query.get(user_id)
            if user:
                print(f"正在删除用户 ID {user_id}: {user.username} ({user.email})")
                db.session.delete(user)
            else:
                print(f"用户 ID {user_id} 不存在")
        
        try:
            db.session.commit()
            print("删除操作已提交")
        except Exception as e:
            db.session.rollback()
            print(f"删除失败: {e}")

if __name__ == '__main__':
    # 删除 ID 为 3, 4, 5 的用户
    delete_users([3, 4, 5])
