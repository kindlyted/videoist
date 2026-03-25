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


def generate_activation_token():
    """生成激活token"""
    import secrets
    import string
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))


def send_activation_email(email: str, token: str):
    """发送账户激活邮件"""
    if not RESEND_API_KEY:
        raise Exception("RESEND_API_KEY not configured")

    # 构建激活URL - 这里需要根据你的前端域名调整
    activation_url = f"http://localhost:5173/activate?token={token}"

    resend.api_key = RESEND_API_KEY

    params = {
        "from": f"{MAIL_FROM_NAME} <{MAIL_FROM_EMAIL}>",
        "to": [email],
        "subject": "【Videoist】请激活您的账户",
        "html": f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 500px; margin: 0 auto; padding: 20px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .btn {{ background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; }}
                .btn:hover {{ background: #1d4ed8; }}
                .footer {{ text-align: center; font-size: 12px; color: #666; margin-top: 30px; }}
                .code-box {{ background: #f5f5f5; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
                .token {{ font-family: monospace; background: #e5e7eb; padding: 8px; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>欢迎加入 Videoist</h1>
                </div>
                <p>您好，</p>
                <p>您已成功注册 Videoist 账户，请点击下方按钮激活您的账户：</p>
                <a href="{activation_url}" class="btn">激活账户</a>
                <p style="margin-top: 20px;">如果按钮无法点击，请复制以下链接到浏览器：</p>
                <div class="code-box">
                    <span class="token">{activation_url}</span>
                </div>
                <p>此链接将在 <strong>24小时</strong> 后失效。</p>
                <p>如有问题，请联系客服。</p>
                <div class="footer">
                    <p>此邮件由 Videoist 系统自动发送，请勿回复。</p>
                    <p>&copy; 2026 Videoist. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
    }

    response = resend.Emails.send(params)
    return response


def send_verification_email(email: str, code: str):
    """发送验证码邮件（保留用于登录验证）"""
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

    response = resend.Emails.send(params)
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
