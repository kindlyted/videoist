#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import app, db
from models import User

def check_users():
    """检查数据库中的用户"""
    with app.app_context():
        users = User.query.all()
        print(f"数据库中共有 {len(users)} 个用户:")
        print("-" * 50)
        for user in users:
            print(f"ID: {user.id}")
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            print(f"是否激活: {user.is_active}")
            print(f"是否管理员: {user.is_admin}")
            print(f"密码哈希: {'已设置' if user.password_hash else '未设置'}")
            print("-" * 50)

if __name__ == '__main__':
    check_users()