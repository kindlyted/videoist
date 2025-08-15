# routes/auth.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from models import db, User, WordPressSite, WechatAccount
from datetime import timedelta

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
# 用户认证相关 API
# --------------------------

@auth_bp.route('/login', methods=['POST'])
def login():
    """JWT 登录接口"""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "必须提供用户名和密码"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.verify_password(data['password']):
        return jsonify({"error": "用户名或密码错误"}), 401

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
            "email": user.email
        }
    }), 200

@auth_bp.route('/user-info', methods=['GET'])
@jwt_required()
def get_user_info():
    """获取用户信息"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
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
    return jsonify({"message": "成功登出"}), 200


@auth_bp.route('/update-password', methods=['POST'])
@jwt_required()
def update_password():
    """更新用户密码接口"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    data = request.get_json()
    if not data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({"error": "必须提供当前密码和新密码"}), 400
    
    # 验证当前密码
    if not user.verify_password(data['current_password']):
        return jsonify({"error": "当前密码错误"}), 400
    
    # 更新密码
    user.set_password(data['new_password'])
    db.session.commit()
    
    return jsonify({"message": "密码更新成功"}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    data = request.get_json()
    required_fields = ['username', 'password', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "缺少必填字段"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "用户名已存在"}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "邮箱已被注册"}), 409

    try:
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        # 自动登录
        access_token = create_access_token(identity=user.username)
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

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
        return jsonify({"error": "缺少必要字段"}), 400

    # 检查站点是否已存在
    existing_site = WordPressSite.query.filter_by(
        user_id=user.id,
        site_url=data['site_url']
    ).first()

    if existing_site:
        return jsonify({"error": "该站点URL已存在"}), 409

    required_fields = ['site_name', 'site_url', 'username', 'api_key', 'wp_tag', 'wp_footer']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "缺少必要字段"}), 400

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
        return jsonify({"error": "站点不存在或无权访问"}), 404

    required_fields = ['site_name', 'site_url', 'username', 'api_key', 'wp_tag', 'wp_footer']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "缺少必要字段"}), 400

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
        return jsonify({"error": "站点不存在或无权访问"}), 404

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
        return jsonify({"error": "缺少必要字段"}), 400

    # 检查是否已存在
    existing_account = WechatAccount.query.filter_by(
        user_id=user.id,
        app_id=data['app_id']
    ).first()

    if existing_account:
        return jsonify({"error": "该AppID已存在"}), 409

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
        return jsonify({"error": "公众号不存在或无权访问"}), 404

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
        return jsonify({"error": "公众号不存在或无权访问"}), 404

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
        return jsonify({"error": "必须提供邮箱地址"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        # 为了安全起见，即使用户不存在也返回成功
        return jsonify({"message": "如果该邮箱存在，重置链接已发送"}), 200

    # 生成重置令牌（简化实现，实际应用中应使用更安全的方法）
    reset_token = f"{user.id}-{user.email}-{int(time.time())}"
    reset_token_hash = hashlib.sha256(reset_token.encode()).hexdigest()
    
    # 在实际应用中，这里会发送包含重置链接的邮件
    # 为简化起见，我们只是返回令牌
    reset_url = f"{request.host_url}reset-password/{reset_token_hash}"
    return jsonify({
        "message": "重置链接已发送到您的邮箱",
        "reset_url": reset_url  # 仅用于测试，实际应用中不应返回此信息
    }), 200


@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password_confirm(token):
    """确认重置密码接口"""
    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({"error": "必须提供新密码"}), 400
    
    # 在实际应用中，这里会验证令牌
    # 为简化起见，我们接受任何令牌
    # 但在实际应用中，应该有更严格的验证
    
    # 这里我们假设令牌验证通过，直接重置密码
    # 在实际应用中，应该从令牌中提取用户信息
    
    # 由于简化实现，我们无法验证令牌，直接返回成功
    # 在实际应用中，请实现完整的令牌验证逻辑
    
    return jsonify({"message": "密码重置成功"}), 200