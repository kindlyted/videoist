import re
from pathlib import Path
from typing import Dict, Any
from config import Config

class PromptRenderer:
    """轻量级模板渲染引擎（方案A优化版）"""
    
    def __init__(self):
        """
        初始化渲染器，不再固定模板目录
        """
        self._cache = {}  # 模板缓存
        
    def _load_template(self, template_dir: Path, name: str) -> str:
        """加载模板文件（带缓存机制）
        
        Args:
            template_dir: 模板文件目录路径
            name: 模板名称
        """
        cache_key = f"{template_dir}_{name}"  # 使用目录+名称作为缓存键
        if cache_key not in self._cache:
            path = template_dir / f"{name}.prompt"
            with open(path, 'r', encoding='utf-8') as f:
                self._cache[cache_key] = f.read()
        return self._cache[cache_key]
    
    def render(
        self,
        template_dir: str,
        template_name: str,
        context: Dict[str, Any],
        strict: bool = True
    ) -> str:
        """
        渲染模板
        
        Args:
            template_dir: 模板文件存放目录
            template_name: 模板文件名（不含扩展名）
            context: 变量字典
            strict: 是否严格检查所有占位符都有对应值
            
        Returns:
            渲染后的文本
        """
        template_dir = Path(template_dir)
        template = self._load_template(template_dir, template_name)
        
        if strict:
            # 检查所有占位符是否都有提供值
            placeholders = set(re.findall(r"%%(\w+)%%", template))
            missing = placeholders - set(context.keys())
            if missing:
                raise ValueError(f"Missing values for placeholders: {missing}")
        
        # 按变量名长度降序替换，避免短变量名被部分替换
        for key in sorted(context.keys(), key=len, reverse=True):
            template = template.replace(f"%%{key}%%", str(context[key]))
            
        return template

    def render_to_file(
        self,
        template_dir: str,
        template_name: str,
        context: Dict[str, Any],
        output_path: str,
        **kwargs
    ) -> None:
        """渲染模板并直接保存到文件
        
        Args:
            template_dir: 模板文件存放目录
            template_name: 模板文件名（不含扩展名）
            context: 变量字典
            output_path: 输出文件路径
        """
        rendered = self.render(template_dir, template_name, context, **kwargs)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
            