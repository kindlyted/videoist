# routes/note.py

import os
from flask import Blueprint, request, url_for, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from services.note.note_core import process_pdf_to_png
from config import Config
from models import Note, User
from extensions import db
from services.common.error_codes import ErrorCode
from services.common.utils import get_error_message, create_error_response, create_success_response

# 创建蓝图
note_bp = Blueprint('note', __name__)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@note_bp.route('/notes-generator', methods=['POST'])
@jwt_required()
def upload_file():
    # user_id = get_jwt_identity()
    # user = User.query.get(user_id)
    
    if 'file' not in request.files:
        current_app.logger.error("未接收到文件字段")
        return jsonify(create_error_response(ErrorCode.NO_FILE_SELECTED)), 400
    
    file = request.files['file']
    if file.filename == '':
        current_app.logger.error("文件名为空")
        return jsonify(create_error_response(ErrorCode.NO_FILE_SELECTED)), 400
    
    if not allowed_file(file.filename):
        current_app.logger.error(f"文件类型不支持: {file.filename}")
        return jsonify(create_error_response(ErrorCode.UNSUPPORTED_FILE_TYPE)), 400
    
    try:
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'storage', 'input')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        

        prompt_path = str(Config.PROMPT_DIR / "keshihua0.prompt")
        output_dir = os.path.join(current_app.root_path, 'storage', 'note_output')
        os.makedirs(output_dir, exist_ok=True)
        output_pic_path, desc = process_pdf_to_png(file_path, prompt_path, output_dir)

        # 保存note信息到数据库
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify(create_error_response(ErrorCode.USER_NOT_FOUND)), 404

        note = Note(
            title=filename,  # 使用上传的PDF文件名作为标题
            description=desc[:200] if desc else '',  # 取描述文本的前200个字符
            image_path=url_for('storage_files', filename=f'note_output/{os.path.basename(output_pic_path)}'),
            user_id=user.id  # 显式设置user_id
        )
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': get_error_message(ErrorCode.FILE_PROCESSING_SUCCESS),
            'image_url': url_for('storage_files', filename=f'note_output/{os.path.basename(output_pic_path)}')
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"处理文件时出错: {str(e)}")
        return jsonify(create_error_response(ErrorCode.INTERNAL_SERVER_ERROR)), 500

@note_bp.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    # 获取当前用户
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    notes = Note.query.filter_by(user_id=user.id).order_by(Note.created_at.desc()).all()
    
    notes_data = []
    for note in notes:
        notes_data.append({
            'id': note.id,
            'title': note.title,
            'description': note.description,
            'image_url': note.image_path,
            'created_at': note.created_at.isoformat()
        })
    
    return jsonify({
        'success': True,
        'data': notes_data
    })

@note_bp.route('/note/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note_detail(note_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    note = Note.query.filter_by(id=note_id, user_id=user.id).first_or_404()
    
    return jsonify({
        'success': True,
        'data': {
            'id': note.id,
            'title': note.title,
            'description': note.description,
            'image_url': note.image_path,
            'created_at': note.created_at.isoformat()
        }
    })

@note_bp.route('/note/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    """删除指定笔记"""
    # 获取当前用户
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify(create_error_response(ErrorCode.USER_NOT_LOGGED_IN)), 401
        
    # 获取笔记信息
    note = Note.query.get_or_404(note_id)
    
    # 检查笔记是否属于当前用户
    if note.user_id != user.id:
        return jsonify(create_error_response(ErrorCode.UNAUTHORIZED_NOTE_DELETION)), 403
    
    # 删除笔记
    db.session.delete(note)
    db.session.commit()
    
    return jsonify(create_success_response(ErrorCode.NOTE_DELETION_SUCCESS))

@note_bp.route('/note-stats', methods=['GET'])
@jwt_required()
def get_note_stats():
    """获取笔记统计数据（笔记总数）"""
    try:
        # 获取当前用户名
        current_username = get_jwt_identity()
        
        # 根据用户名查询用户ID
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify(create_error_response(ErrorCode.USER_NOT_FOUND)), 404
        
        # 使用用户ID查询笔记数量
        note_count = Note.query.filter_by(user_id=user.id).count()
        
        return jsonify({
            'note_count': note_count
        })
    except Exception as e:
        return jsonify(create_error_response(ErrorCode.NOTE_STATS_ERROR, str(e))), 500
