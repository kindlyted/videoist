# services/common/email_service.py
import os
import resend
import secrets
import string
from datetime import datetime, timedelta

# 从环境变量获取配置
RESEND_API_KEY = os.getenv('API_KEY_RESEND')
MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME', 'Videoist')
MAIL_FROM_EMAIL = os.getenv('MAIL_FROM_EMAIL', 'onboarding@resend.dev')

# 验证码存储（生产环境应使用Redis）
verification_codes = {}


def generate_verification_code(length=6):
    """生成6位数字验证码"""
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def send_verification_email(email: str, code: str):
    """发送验证码邮件"""
    if not RESEND_API_KEY:
        raise Exception("RESEND_API_KEY not configured")

    resend.api_key = RESEND_API_KEY

    params = {
        "from": f"{MAIL_FROM_NAME} <{MAIL_FROM_EMAIL}>",
        "to": [email],
        "subject": "【Videoist】您的登录验证码",
        "html": f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 500px; margin: 0 auto; padding: 20px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .code-box {{ background: #f5f5f5; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
                .code {{ font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #2563eb; }}
                .footer {{ text-align: center; font-size: 12px; color: #666; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Videoist</h1>
                </div>
                <p>您好，</p>
                <p>您的登录验证码如下，请尽快完成验证。验证码有效期为 <strong>10 分钟</strong>。</p>
                <div class="code-box">
                    <span class="code">{code}</span>
                </div>
                <p>如果这不是您的操作，请忽略此邮件。</p>
                <div class="footer">
                    <p>此邮件由 Videoist 系统自动发送，请勿回复。</p>
                </div>
            </div>
        </body>
        </html>
        """
    }

    response = resend.Email.send(params)
    return response


def store_verification_code(email: str, code: str, expires_minutes=10):
    """存储验证码，设置过期时间"""
    verification_codes[email] = {
        'code': code,
        'expires_at': datetime.utcnow() + timedelta(minutes=expires_minutes),
        'attempts': 0
    }


def verify_code(email: str, code: str, max_attempts=5):
    """验证验证码"""
    if email not in verification_codes:
        return False, "验证码已过期，请重新获取"

    stored = verification_codes[email]

    # 检查尝试次数
    if stored['attempts'] >= max_attempts:
        del verification_codes[email]
        return False, "验证码尝试次数过多，请重新获取"

    # 检查过期
    if datetime.utcnow() > stored['expires_at']:
        del verification_codes[email]
        return False, "验证码已过期，请重新获取"

    # 验证验证码
    if stored['code'] != code:
        stored['attempts'] += 1
        return False, "验证码错误"

    # 验证成功，删除验证码
    del verification_codes[email]
    return True, "验证成功"


def send_and_store_code(email: str):
    """发送验证码并存储"""
    code = generate_verification_code()
    send_verification_email(email, code)
    store_verification_code(email, code)
    return code
