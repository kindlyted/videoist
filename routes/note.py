# routes/note.py

import os
from flask import Blueprint, request, url_for, jsonify, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from services.note.note_core import process_pdf_to_png
from config import Config

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
    if 'file' not in request.files:
        current_app.logger.error("未接收到文件字段")
        return jsonify({'success': False, 'message': '未选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        current_app.logger.error("文件名为空")
        return jsonify({'success': False, 'message': '未选择文件'}), 400
    
    if not allowed_file(file.filename):
        current_app.logger.error(f"文件类型不支持: {file.filename}")
        return jsonify({'success': False, 'message': '仅支持PDF文件'}), 400
    
    try:
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'storage', 'input')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        

        prompt_path = str(Config.PROMPT_DIR / "keshihua0.prompt")
        output_dir = os.path.join(current_app.root_path, 'storage', 'note_output')
        os.makedirs(output_dir, exist_ok=True)
        output_pic_path = process_pdf_to_png(file_path, prompt_path, output_dir)
        
        return jsonify({
            'success': True,
            'message': '文件处理成功',
            'image_url': url_for('storage_files', filename=f'note_output/{os.path.basename(output_pic_path)}')
        })
    except Exception as e:
        current_app.logger.error(f"处理文件时出错: {str(e)}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500
