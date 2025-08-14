# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
from extensions import db, migrate
from config import Config, config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__, instance_path=str(Config.INSTANCE_DIR))
    app.config.from_object(config.get(os.getenv('FLASK_ENV', 'default')))
    
    # 确保正确解析JSON请求
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # 配置静态文件服务，使storage目录下的文件可以通过HTTP访问
    @app.route('/storage/<path:filename>', endpoint='storage_files')
    def storage_files(filename):
        return send_from_directory(Config.STORAGE_FOLDER, filename)

    # 从环境变量获取允许的域名列表
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173').split(',')
    # 配置 CORS，只允许特定域名访问
    CORS(app, resources={
        r"/*": {
            "origins": ALLOWED_ORIGINS,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # 确保正确处理JSON请求
    @app.before_request
    def handle_json():
        # 处理OPTIONS请求
        if request.method == 'OPTIONS':
            return None
        
        if request.method in ['POST', 'PUT', 'PATCH'] and request.content_type == 'application/json':
            try:
                request.get_json()
            except Exception:
                pass  # 忽略解析错误，让路由处理函数自己处理

    # 确保instance目录存在
    Path(app.instance_path).mkdir(exist_ok=True)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    
    # 配置JWT密钥
    app.config['JWT_SECRET_KEY'] = app.config.get('JWT_SECRET_KEY')
    
    # 配置JWT错误处理器
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token已过期',
            'message': '请重新登录'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': '无效的Token',
            'message': '请重新登录'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': '缺少Token',
            'message': '请先登录'
        }), 401
    
    # 注册蓝图
    from routes.auth import auth_bp
    from routes.video import video_bp
    from routes.note import note_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(note_bp)
    
    return app

# 显式创建app实例以支持flask命令
app = create_app()

if __name__ == '__main__':
    print("\n应用启动信息:")
    print(f"服务地址: http://localhost:5010")
    app.run(host='0.0.0.0', port=5010, debug=app.config.get('DEBUG'))