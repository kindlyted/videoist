# models.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db  # 从统一的extensions导入db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)  # Google登录时可选
    email = db.Column(db.String(120), unique=True, nullable=False)  # 邮箱是必需的
    password_hash = db.Column(db.String(256), nullable=True)  # 允许为空（第三方登录）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    # OAuth 字段
    google_id = db.Column(db.String(120), unique=True, nullable=True)
    auth_provider = db.Column(db.String(20), default='email')  # 'email', 'google'
    avatar_url = db.Column(db.String(500), nullable=True)

    # 密码处理方法
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        """专门用于设置密码的方法（兼容旧代码）"""
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.username}>'

    @staticmethod
    def generate_username(email=None):
        """生成唯一的用户名"""
        if not email:
            base_username = 'user'
        else:
            base_username = email.split('@')[0]

        # 确保用户名唯一
        username = base_username
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1

        return username

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='articles')

    def __repr__(self):
        return f'<Article {self.title}>'

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(500), nullable=False)
    thumbnail_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

    
    author = db.relationship('User', backref='videos')

    def __repr__(self):
        return f'<Video {self.title}>'

class PlatformConfig(db.Model):
    __tablename__ = 'platform_configs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    config_name = db.Column(db.String(100), nullable=False)
    platform_name = db.Column(db.String(50), nullable=False)  # 'wordpress' or 'wechat'
    config_key = db.Column(db.String(100), nullable=False)
    config_value = db.Column(db.Text, nullable=False)
    environment = db.Column(db.String(20), default='production')  # 'development' or 'production'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='platform_configs')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'platform_name', 'config_key', 'environment', 
                          name='_user_platform_key_env_uc'),
    )

    def __repr__(self):
        return f'<PlatformConfig {self.config_name} for {self.platform_name}>'

class TagMapping(db.Model):
    __tablename__ = 'tag_mappings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform_name = db.Column(db.String(50), nullable=False)  # 'wordpress' or 'wechat'
    mapping_name = db.Column(db.String(100), nullable=False)
    tag_name = db.Column(db.String(100), nullable=False)
    tag_id = db.Column(db.Integer, nullable=False)
    environment = db.Column(db.String(20), default='production')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='tag_mappings')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'platform_name', 'tag_name', 'environment',
                          name='_user_platform_tag_env_uc'),
    )

    def __repr__(self):
        return f'<TagMapping {self.tag_name}->{self.tag_id} for {self.platform_name}>'

class WordPressSite(db.Model):
    __tablename__ = 'wordpress_sites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    site_name = db.Column(db.String(100), nullable=False)
    site_url = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(255), nullable=False)
    wp_tag = db.Column(db.JSON, nullable=True)  # 用于存储标签字典
    wp_footer = db.Column(db.Text, nullable=True)  # 用于存储HTML页脚内容
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('wordpress_sites', lazy='dynamic'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'site_url', 'is_active', name='_user_site_url_active_uc'),
        db.Index('ix_wordpress_sites_user_id', 'user_id'),
        db.Index('ix_wordpress_sites_site_url', 'site_url'),
    )

    def __repr__(self):
        return f'<WordPressSite {self.site_name} ({self.site_url})>'

class WechatAccount(db.Model):
    __tablename__ = 'wechat_accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.String(100), nullable=False)
    app_id = db.Column(db.String(100), nullable=False)
    app_secret = db.Column(db.String(255), nullable=False)
    wx_footer = db.Column(db.Text, nullable=True)  # 用于存储HTML页脚内容
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('wechat_accounts', lazy='dynamic'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'account_id', 'is_active', name='_user_account_id_active_uc'),
        db.Index('ix_wechat_accounts_user_id', 'user_id'),
        db.Index('ix_wechat_accounts_account_id', 'account_id'),
    )

    def __repr__(self):
        return f'<WechatAccount {self.account_name} ({self.account_id})>'

class PlatformCookies(db.Model):
    __tablename__ = 'platform_cookies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform_name = db.Column(db.String(50), nullable=False)  # 'xiaohongshu', 'douyin', 'shipinhao'
    cookies = db.Column(db.JSON, nullable=False)  # 存储cookie数据
    is_valid = db.Column(db.Boolean, default=True)  # cookie是否有效
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 建立与用户的关系
    user = db.relationship('User', backref=db.backref('platform_cookies', lazy='dynamic'))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'platform_name', name='_user_platform_cookies_uc'),
        db.Index('ix_platform_cookies_user_id', 'user_id'),
    )

    def __repr__(self):
        return f'<PlatformCookies {self.platform_name}>'


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(500), nullable=False)  # 存储生成的图片路径
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    author = db.relationship('User', backref='notes')

    def __repr__(self):
        return f'<Note {self.title}>'