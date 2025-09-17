import os
import tempfile
from pathlib import Path
from loguru import logger
from typing import Tuple, Optional
from services.note.pdf_pipeline import PDFPipeline

class PDFProcessor:
    """独立 PDF 处理器（无 MinerU 依赖）"""
    
    def __init__(self):
        self.pipeline = PDFPipeline()
        
    def extract_markdown_from_pdf(self, pdf_path: str, lang: str = 'ch') -> Tuple[bool, Optional[str], Optional[str]]:
        """
        从 PDF 提取结构化文本
        
        Args:
            pdf_path: PDF文件路径
            lang: OCR语言设置，默认中文
            
        Returns:
            Tuple[success, text_content, error_message]
        """
        try:
            with open(pdf_path, 'rb') as f:
                pdf_bytes = f.read()
            
            # 调用本地 pipeline 解析
            result = self.pipeline.parse_pdf(pdf_bytes, lang=lang)
            
            if result["status"] == "success":
                # 合并所有页面文本
                text_content = "\n\n".join(page["text"] for page in result["pages"])
                logger.info(f"Successfully extracted {len(text_content)} characters from PDF")
                return True, text_content, None
            else:
                error_msg = result.get("message", "PDF processing failed")
                logger.error(error_msg)
                return False, None, error_msg
                
        except Exception as e:
            error_msg = f"PDF processing failed: {str(e)}"
            logger.error(error_msg)
            return False, None, error_msg
    
    def is_available(self) -> bool:
        """处理器始终可用"""
        return True