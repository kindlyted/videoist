#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_admin_user():
    """创建默认的管理员用户"""
    with app.app_context():
        # 检查是否已存在admin用户
        admin = User.query.filter_by(email='admin@eg.com').first()
        if admin:
            print("管理员用户已存在")
            return

        # 创建新的管理员用户
        admin = User(
            username='admin',
            email='admin@eg.com',
            password_hash=generate_password_hash('admin123'),
            is_active=True,  # 直接激活，无需邮箱验证
            is_admin=True
        )

        db.session.add(admin)
        db.session.commit()

        print("管理员用户创建成功！")
        print(f"邮箱: admin@eg.com")
        print(f"密码: admin123")

if __name__ == '__main__':
    create_admin_user()