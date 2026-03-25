#!/usr/bin/env python3
"""
测试邮件发送功能
"""

import os
import sys

# 添加项目路径
sys.path.append("c:\\pyproj\\videoist_flask")

from services.common.email_service import send_verification_email

def test_email():
    try:
        # 从环境变量获取配置
        api_key = os.getenv('API_KEY_RESEND')
        from_email = os.getenv('MAIL_FROM_EMAIL')

        if not api_key:
            print("❌ API_KEY_RESEND 未配置")
            return

        # 测试参数
        test_email = "test@example.com"  # 用你的邮箱替换
        test_code = "123456"

        print(f"🔍 尝试发送测试邮件到 {test_email}")
        print(f"📧 发件人: {from_email}")

        # 发送邮件
        response = send_verification_email(test_email, test_code)

        print("✅ 邮件发送成功！")
        print(f"📋 API响应: {response}")

        # 注意：Resend有一个发件频率限制，不能给同一个邮箱频繁发送
        # 如果需要多次测试，请使用不同的邮箱地址

    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")

if __name__ == "__main__":
    test_email()