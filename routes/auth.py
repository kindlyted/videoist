# routes/auth.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from models import db, User, WordPressSite, WechatAccount, PlatformCookies
from datetime import datetime, timedelta
import time
import hashlib
import os
import requests
from services.common.error_codes import ErrorCode, ERROR_MESSAGES_ZH, ERROR_MESSAGES_EN
from services.common.utils import get_error_message, create_error_response, create_success_response
from services.common.email_service import send_and_store_code, verify_code

# 创建蓝图
auth_bp = Blueprint('auth', __name__)


# --------------------------
# 健康检查 API
# --------------------------

@auth_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "message": "Videoist backend is running normally"
    }), 200

# --------------------------
# 账户激活 API
# --------------------------

@auth_bp.route('/activate', methods=['GET'])
def activate_account():
    """账户激活接口"""
    token = request.args.get('token')
    # 获取语言参数，默认中文
    lang = request.args.get('lang', 'zh')
    if lang.startswith('zh'):
        lang = 'zh'
    else:
        lang = 'en'

    if not token:
        return jsonify({
            "success": False,
            "message": get_error_message(ErrorCode.ACTIVATION_INVALID_TOKEN, lang)
        }), 400

    # 查找用户
    user = User.query.filter_by(activation_token=token).first()

    if not user:
        return jsonify({
            "success": False,
            "message": get_error_message(ErrorCode.ACTIVATION_ALREADY_USED, lang)
        }), 400

    if user.is_active:
        return jsonify({
            "success": False,
            "message": get_error_message(ErrorCode.ACTIVATION_ALREADY_ACTIVE, lang)
        }), 400

    # 检查是否过期（24小时）
    if user.activation_expires_at and user.activation_expires_at < datetime.utcnow():
        return jsonify({
            "success": False,
            "message": get_error_message(ErrorCode.ACTIVATION_EXPIRED, lang)
        }), 400

    # 激活账户
    user.is_active = True
    user.activation_token = None
    user.activation_expires_at = None
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "账户激活成功！" if lang == 'zh' else "Account activated successfully!"
    })

@auth_bp.route('/resend-activation', methods=['POST'])
def resend_activation():
    """重新发送激活邮件"""
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({
            "error_code": ErrorCode.MISSING_REQUIRED_FIELDS.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_REQUIRED_FIELDS]
        }), 400

    email = data['email'].strip().lower()
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "用户不存在"
        }), 404

    if user.is_active:
        return jsonify({
            "success": False,
            "message": "账户已激活"
        }), 400

    # 生成新的激活token
    from services.common.email_service import generate_activation_token
    token = generate_activation_token()
    user.activation_token = token
    user.activation_expires_at = datetime.utcnow() + timedelta(hours=24)
    db.session.commit()

    # 发送激活邮件
    try:
        from services.common.email_service import send_activation_email
        send_activation_email(email, token)

        return jsonify({
            "success": True,
            "message": "激活邮件已重新发送"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"发送邮件失败: {str(e)}"
        }), 500

# --------------------------
# 注册相关 API
# --------------------------

@auth_bp.route('/register', methods=['POST'])
def register():
    """邮箱密码注册接口，需要激活"""
    data = request.get_json()
    print(f"Register request data: {data}")
    if not data or 'email' not in data or 'password' not in data:
        print("Error: Missing email or password")
        return jsonify({
            "error_code": ErrorCode.MISSING_REQUIRED_FIELDS.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_REQUIRED_FIELDS]
        }), 400

    email = data['email'].strip().lower()
    password = data['password']

    print(f"Email: {email}, Password length: {len(password)}")

    # 验证邮箱格式
    if '@' not in email:
        print("Error: Invalid email format")
        return jsonify({
            "error_code": ErrorCode.INVALID_EMAIL.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.INVALID_EMAIL]
        }), 400

    # 验证密码强度
    if len(password) < 6:
        print("Error: Password too short")
        return jsonify({
            "error_code": ErrorCode.PASSWORD_TOO_SHORT.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.PASSWORD_TOO_SHORT]
        }), 400

    # 检查邮箱是否已存在
    if User.query.filter_by(email=email).first():
        print("Error: Email already exists")
        return jsonify({
            "error_code": ErrorCode.EMAIL_EXISTS.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.EMAIL_EXISTS]
        }), 400

    # 生成激活token
    from services.common.email_service import generate_activation_token
    token = generate_activation_token()

    # 创建用户（未激活状态）
    user = User(
        email=email,
        auth_provider='email',
        activation_token=token,
        activation_expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    user.set_password(password)

    # 生成用户名
    username = User.generate_username(email)
    user.username = username

    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Database commit error: {e}")
        return jsonify({
            "success": False,
            "message": f"注册失败: {str(e)}"
        }), 500

    # 发送激活邮件
    try:
        from services.common.email_service import send_activation_email
        send_activation_email(email, token)

        return jsonify({
            "success": True,
            "message": "注册成功！请查收邮件并激活账户。",
            "user_id": user.id
        })
    except Exception as e:
        # 如果邮件发送失败，回滚用户创建
        db.session.rollback()
        print(f"Email send error: {e}")
        return jsonify({
            "success": False,
            "message": f"注册失败，发送激活邮件失败: {str(e)}"
        }), 500

# --------------------------
# 用户认证相关 API
# --------------------------

@auth_bp.route('/login', methods=['POST'])
def login():
    """支持邮箱验证码登录和邮箱密码登录"""
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({
            "error_code": ErrorCode.MISSING_REQUIRED_FIELDS.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_REQUIRED_FIELDS]
        }), 400

    email = data['email'].strip().lower()
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "error_code": ErrorCode.USER_NOT_FOUND.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.USER_NOT_FOUND]
        }), 404

    # 检查账户是否激活
    if not user.is_active:
        return jsonify({
            "error_code": ErrorCode.ACCOUNT_NOT_ACTIVATED.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.ACCOUNT_NOT_ACTIVATED]
        }), 401

    # 如果使用验证码登录
    if 'code' in data:
        code = data['code'].strip()
        # 验证验证码
        is_valid, message = verify_code(email, code)
        if not is_valid:
            return jsonify({
                "error_code": ErrorCode.INVALID_VERIFICATION_CODE.value,
                "message": message
            }), 400

    # 如果使用密码登录
    elif 'password' in data:
        password = data['password']
        if not user.verify_password(password):
            return jsonify({
                "error_code": ErrorCode.INVALID_PASSWORD.value,
                "message": ERROR_MESSAGES_ZH[ErrorCode.INVALID_PASSWORD]
            }), 401
    else:
        return jsonify({
            "error_code": ErrorCode.MISSING_REQUIRED_FIELDS.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_REQUIRED_FIELDS]
        }), 400

    # 生成 Token（有效期7天）
    access_token = create_access_token(
        identity=user.username,
        expires_delta=timedelta(days=7)
    )
    refresh_token = create_refresh_token(identity=user.username)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "auth_provider": user.auth_provider
        }
    }), 200

@auth_bp.route('/user-info', methods=['GET'])
@jwt_required()
def get_user_info():
    """获取用户信息"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({
            "error_code": ErrorCode.USER_NOT_FOUND.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.USER_NOT_FOUND]
        }), 404

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "auth_provider": user.auth_provider,
            "avatar_url": user.avatar_url
        }
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """刷新 Access Token"""
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify({"access_token": new_token}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """JWT 登出接口"""
    # 在实际应用中，你可能想要将token加入黑名单
    # 但在这个简单的实现中，我们只需要返回成功响应
    # 前端会负责删除本地存储的token
    return jsonify(create_success_response(ErrorCode.LOGOUT_SUCCESS)), 200

@auth_bp.route('/check-platform-login', methods=['GET'])
@jwt_required()
def check_platform_login():
    """检查平台登录状态"""
    platform = request.args.get('platform')
    if not platform:
        return jsonify({
            "error_code": ErrorCode.INVALID_PLATFORM.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.INVALID_PLATFORM]
        }), 400
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({
            "error_code": ErrorCode.USER_NOT_FOUND.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.USER_NOT_FOUND]
        }), 404
    
    # 检查数据库中是否存在有效的cookies
    platform_cookies = PlatformCookies.query.filter_by(
        user_id=user.id,
        platform_name=platform,
        is_valid=True
    ).first()
    
    return jsonify({
        "is_logged_in": platform_cookies is not None,
        "platform": platform
    })


@auth_bp.route('/update-password', methods=['POST'])
@jwt_required()
def update_password():
    """更新用户密码接口"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify(create_error_response(ErrorCode.USER_NOT_FOUND)), 404

    if user.auth_provider != 'password':
        return jsonify({
            "error_code": ErrorCode.PASSWORD_NOT_SUPPORTED.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.PASSWORD_NOT_SUPPORTED]
        }), 400

    data = request.get_json()
    if not data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({
            "error_code": ErrorCode.MISSING_REQUIRED_FIELDS.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_REQUIRED_FIELDS]
        }), 400

    # 验证当前密码
    if not user.verify_password(data['current_password']):
        return jsonify({
            "error_code": ErrorCode.CURRENT_PASSWORD_ERROR.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.CURRENT_PASSWORD_ERROR]
        }), 400

    # 更新密码
    user.set_password(data['new_password'])
    user.auth_provider = 'password'  # 确保标记为密码登录
    db.session.commit()

    return jsonify(create_success_response(ErrorCode.PASSWORD_UPDATE_SUCCESS)), 200

# 密码注册接口已移除，使用邮箱验证码注册
# @auth_bp.route('/register', methods=['POST'])
# def register():
#     """用户注册接口（已废弃，使用邮箱验证码注册）"""
#     return jsonify({
#         "error_code": ErrorCode.METHOD_NOT_SUPPORTED.value,
#         "message": "Password registration is disabled, please use email verification"
#     }), 400


# --------------------------
# 邮箱验证码登录/注册 API
# --------------------------

@auth_bp.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    """发送邮箱验证码"""
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({
            "error_code": ErrorCode.MISSING_EMAIL.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_EMAIL]
        }), 400

    email = data['email'].strip().lower()

    try:
        send_and_store_code(email)
        return jsonify(create_success_response("验证码已发送")), 200
    except Exception as e:
        return jsonify({
            "error_code": ErrorCode.EMAIL_SEND_FAILED.value,
            "message": f"发送验证码失败: {str(e)}"
        }), 500


@auth_bp.route('/verify-and-login', methods=['POST'])
def verify_and_login():
    """邮箱验证码验证并登录（支持注册和登录）"""
    data = request.get_json()
    if not data or 'email' not in data or 'code' not in data:
        return jsonify({
            "error_code": ErrorCode.MISSING_REQUIRED_FIELDS.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_REQUIRED_FIELDS]
        }), 400

    email = data['email'].strip().lower()
    code = data['code'].strip()

    # 验证验证码
    is_valid, message = verify_code(email, code)
    if not is_valid:
        return jsonify({
            "error_code": ErrorCode.INVALID_VERIFICATION_CODE.value,
            "message": message
        }), 400

    # 查找或创建用户
    user = User.query.filter_by(email=email).first()

    if not user:
        # 新用户，自动注册
        # 生成用户名（使用邮箱前缀）
        username = email.split('@')[0]
        # 确保用户名唯一
        base_username = username
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1

        user = User(
            username=username,
            email=email,
            auth_provider='email'
        )
        db.session.add(user)
        db.session.commit()

    # 生成 Token
    access_token = create_access_token(
        identity=user.username,
        expires_delta=timedelta(days=7)
    )

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "auth_provider": user.auth_provider
        }
    }), 200


# --------------------------
# Google OAuth 登录 API
# --------------------------

@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    """Google OAuth 登录（使用access_token）"""
    data = request.get_json()
    if not data or 'access_token' not in data:
        return jsonify({
            "error_code": ErrorCode.MISSING_REQUIRED_FIELDS.value,
            "message": "Missing access_token"
        }), 400

    access_token = data['access_token']

    try:
        # 使用 Google API 验证 access_token
        google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        if not google_client_id or google_client_id == 'your-google-client-id':
            return jsonify({
                "error_code": ErrorCode.SYSTEM_ERROR.value,
                "message": "Google OAuth not configured"
            }), 500

        # 验证 access_token
        userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(userinfo_url, headers=headers)
        if response.status_code != 200:
            return jsonify({
                "error_code": ErrorCode.INVALID_TOKEN.value,
                "message": "Invalid Google token"
            }), 401

        userinfo = response.json()

        # 验证 audience
        if userinfo.get('hd') and 'google.com' in userinfo.get('hd'):
            # 验证域名
            pass

        google_id = userinfo.get('id')
        email = userinfo.get('email')
        name = userinfo.get('name', '')
        picture = userinfo.get('picture')

        if not email or not google_id:
            return jsonify({
                "error_code": ErrorCode.INVALID_TOKEN.value,
                "message": "Invalid token payload"
            }), 401

        # 查找或创建用户
        user = User.query.filter_by(google_id=google_id).first()

        if not user:
            # 检查邮箱是否已存在
            user = User.query.filter_by(email=email).first()
            if user:
                # 已存在邮箱用户，关联Google ID
                user.google_id = google_id
                user.auth_provider = 'google'
                if user.avatar_url and picture:
                    user.avatar_url = picture
            else:
                # 新用户，创建
                username = email.split('@')[0]
                base_username = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1

                user = User(
                    username=username,
                    email=email,
                    google_id=google_id,
                    auth_provider='google',
                    avatar_url=picture
                )
                db.session.add(user)

            db.session.commit()

        # 生成 Token
        access_token = create_access_token(
            identity=user.username,
            expires_delta=timedelta(days=7)
        )

        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "auth_provider": user.auth_provider,
                "avatar_url": user.avatar_url
            }
        }), 200

    except Exception as e:
        return jsonify({
            "error_code": ErrorCode.SYSTEM_ERROR.value,
            "message": f"Google login failed: {str(e)}"
        }), 500


# --------------------------
# WordPress 管理 API
# --------------------------

@auth_bp.route('/wordpress', methods=['GET'])
@jwt_required()
def list_wordpress_sites():
    """获取用户的 WordPress 站点列表"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    sites = WordPressSite.query.filter_by(
        user_id=user.id,
        is_active=True
    ).all()

    return jsonify([{
        "id": site.id,
        "site_name": site.site_name,
        "site_url": site.site_url,
        "username": site.username,
        "wp_tag": site.wp_tag,
        "wp_footer": site.wp_footer
        # 不返回敏感字段api_key
    } for site in sites]), 200

@auth_bp.route('/wordpress', methods=['POST'])
@jwt_required()
def add_wordpress_site():
    """添加 WordPress 站点"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    data = request.get_json()

    required_fields = ['site_name', 'site_url', 'username', 'api_key']
    if not all(field in data for field in required_fields):
        return jsonify({
            "error_code": ErrorCode.MISSING_REQUIRED_FIELDS.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_REQUIRED_FIELDS]
        }), 400

    # 检查站点是否已存在
    existing_site = WordPressSite.query.filter_by(
        user_id=user.id,
        site_url=data['site_url']
    ).first()

    if existing_site:
        return jsonify({
            "error_code": ErrorCode.WORDPRESS_SITE_EXISTS.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.WORDPRESS_SITE_EXISTS]
        }), 409

    required_fields = ['site_name', 'site_url', 'username', 'api_key', 'wp_tag', 'wp_footer']
    if not all(field in data for field in required_fields):
        return jsonify(create_error_response(ErrorCode.MISSING_REQUIRED_FIELDS)), 400

    try:
        site = WordPressSite(
            site_name=data['site_name'],
            site_url=data['site_url'],
            username=data['username'],
            api_key=data['api_key'],
            wp_tag=data['wp_tag'],
            wp_footer=data['wp_footer'],
            user_id=user.id
        )
        db.session.add(site)
        db.session.commit()
        return jsonify({"id": site.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/wordpress/<int:site_id>', methods=['PUT'])
@jwt_required()
def update_wordpress_site(site_id):
    """更新 WordPress 站点"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    data = request.get_json()

    site = WordPressSite.query.filter_by(
        id=site_id,
        user_id=user.id
    ).first()

    if not site:
        return jsonify({
            "error_code": ErrorCode.WORDPRESS_SITE_NOT_FOUND.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.WORDPRESS_SITE_NOT_FOUND]
        }), 404

    required_fields = ['site_name', 'site_url', 'username', 'api_key', 'wp_tag', 'wp_footer']
    if not all(field in data for field in required_fields):
        return jsonify(create_error_response(ErrorCode.MISSING_REQUIRED_FIELDS)), 400

    try:
        # 更新站点信息
        site.site_name = data['site_name']
        site.site_url = data['site_url']
        site.username = data['username']
        site.api_key = data['api_key']
        site.wp_tag = data['wp_tag']
        site.wp_footer = data['wp_footer']
            
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/wordpress/<int:site_id>', methods=['DELETE'])
@jwt_required()
def delete_wordpress_site(site_id):
    """删除 WordPress 站点（软删除）"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    site = WordPressSite.query.filter_by(
        id=site_id,
        user_id=user.id
    ).first()

    if not site:
        return jsonify(create_error_response(ErrorCode.WORDPRESS_SITE_NOT_FOUND)), 404

    try:
        site.is_active = False
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# --------------------------
# 微信公众号管理 API
# --------------------------

@auth_bp.route('/wechat', methods=['GET'])
@jwt_required()
def list_wechat_accounts():
    """获取微信公众号列表"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    accounts = WechatAccount.query.filter_by(
        user_id=user.id,
        is_active=True
    ).all()

    return jsonify([{
        "id": account.id,
        "account_name": account.account_name,
        "account_id": account.account_id,
        "app_id": account.app_id,
        "wx_footer": account.wx_footer
        # 不返回敏感字段app_secret
    } for account in accounts]), 200

@auth_bp.route('/wechat', methods=['POST'])
@jwt_required()
def add_wechat_account():
    """添加微信公众号"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    data = request.get_json()

    required_fields = ['account_name', 'account_id', 'app_id', 'app_secret']
    if not all(field in data for field in required_fields):
        return jsonify(create_error_response(ErrorCode.MISSING_REQUIRED_FIELDS)), 400

    # 检查是否已存在
    existing_account = WechatAccount.query.filter_by(
        user_id=user.id,
        app_id=data['app_id']
    ).first()

    if existing_account:
        return jsonify(create_error_response(ErrorCode.WECHAT_APPID_EXISTS)), 409

    try:
        account = WechatAccount(
            account_name=data['account_name'],
            account_id=data['account_id'],
            app_id=data['app_id'],
            app_secret=data['app_secret'],  # 敏感字段，确保传输过程中使用HTTPS
            wx_footer=data.get('wx_footer'),
            user_id=user.id
        )
        db.session.add(account)
        db.session.commit()
        return jsonify({"id": account.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/wechat/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_wechat_account(account_id):
    """更新微信公众号"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    data = request.get_json()

    account = WechatAccount.query.filter_by(
        id=account_id,
        user_id=user.id
    ).first()

    if not account:
        return jsonify({
            "error_code": ErrorCode.WECHAT_ACCOUNT_NOT_FOUND.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.WECHAT_ACCOUNT_NOT_FOUND]
        }), 404

    try:
        # 更新公众号信息
        if 'account_name' in data:
            account.account_name = data['account_name']
        if 'account_id' in data:
            account.account_id = data['account_id']
        if 'app_id' in data:
            account.app_id = data['app_id']
        if 'app_secret' in data:
            account.app_secret = data['app_secret']  # 敏感字段，确保传输过程中使用HTTPS
        if 'wx_footer' in data:
            account.wx_footer = data['wx_footer']
            
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/wechat/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_wechat_account(account_id):
    """删除微信公众号（软删除）"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    account = WechatAccount.query.filter_by(
        id=account_id,
        user_id=user.id
    ).first()

    if not account:
        return jsonify({
            "error_code": ErrorCode.WECHAT_ACCOUNT_NOT_FOUND.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.WECHAT_ACCOUNT_NOT_FOUND]
        }), 404

    try:
        account.is_active = False
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# --------------------------
# 密码重置 API
# --------------------------

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """重置密码接口"""
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({
            "error_code": ErrorCode.MISSING_EMAIL.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_EMAIL]
        }), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        # 为了安全起见，即使用户不存在也返回成功
        return jsonify(create_success_response(ErrorCode.PASSWORD_RESET_EMAIL_SENT)), 200

    # 生成重置令牌（简化实现，实际应用中应使用更安全的方法）
    reset_token = f"{user.id}-{user.email}-{int(time.time())}"
    reset_token_hash = hashlib.sha256(reset_token.encode()).hexdigest()
    
    # 在实际应用中，这里会发送包含重置链接的邮件
    # 为简化起见，我们只是返回令牌
    reset_url = f"{request.host_url}reset-password/{reset_token_hash}"
    return jsonify({
        "message": get_error_message(ErrorCode.PASSWORD_RESET_EMAIL_SENT),
        "reset_url": reset_url  # 仅用于测试，实际应用中不应返回此信息
    }), 200


@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password_confirm(token):
    """确认重置密码接口"""
    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({
            "error_code": ErrorCode.MISSING_PASSWORD.value,
            "message": ERROR_MESSAGES_ZH[ErrorCode.MISSING_PASSWORD]
        }), 400
    
    # 在实际应用中，这里会验证令牌
    # 为简化起见，我们接受任何令牌
    # 但在实际应用中，应该有更严格的验证
    
    # 这里我们假设令牌验证通过，直接重置密码
    # 在实际应用中，应该从令牌中提取用户信息
    
    # 由于简化实现，我们无法验证令牌，直接返回成功
    # 在实际应用中，请实现完整的令牌验证逻辑
    
    return jsonify(create_success_response(ErrorCode.PASSWORD_RESET_SUCCESS)), 200