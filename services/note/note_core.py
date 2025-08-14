import os
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from services.common.utils import invoke_with_attachment_qwen, invoke_with_attachment_kimi

# 使用 BeautifulSoup 清理 HTML
def save_html(html_content, output_path) -> None:
    # 1. 先提取 <!DOCTYPE html> ... </html> 之间的内容
    start = html_content.find('<!DOCTYPE html>')
    end = html_content.rfind('</html>')
    
    if start == -1 or end == -1:
        print("警告：未找到完整的 HTML 结构，可能输出不完整内容")
        extracted = html_content  # 保留原始内容（或抛出异常）
    else:
        extracted = html_content[start:end+7]  # +7 是 </html> 的长度
    
    # 2. 用 BeautifulSoup 清理并规范化
    soup = BeautifulSoup(extracted, 'html.parser')
    cleaned_html = str(soup)
    
    # 3. 输出检查并保存文件
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)
    print("已生成文件:", output_path)

# 创建封面postist和videoist共用，playwright替代selenium
def save_note_pic(html_file_path, picture_filename) -> None:
    from pathlib import Path
    
    # 转换为 Path 对象
    html_path = Path(html_file_path)
    
    # 检查文件是否存在
    if not html_path.exists():
        print(f"错误：文件 {html_path} 不存在")
        return
    
    # 使用 Playwright 替代 Selenium
    with sync_playwright() as p:
        # 启动浏览器（Playwright 会自动下载浏览器，无需单独配置驱动）
        browser = p.chromium.launch(headless=True)  # 无头模式
        page = browser.new_page()
        
        try:
            # 打开HTML文件（使用绝对路径）
            page.set_viewport_size({"width": 1200, "height": 1600})
            page.goto(f'file://{html_path.absolute()}')
            
            # 等待元素加载（Playwright 有更简洁的等待方式）
            page.locator('footer').wait_for()
            
            # 获取页面截图
            page.screenshot(
                path=picture_filename,
                full_page=True,
                type='png'
            )
            
        except Exception as e:
            print(f"发生错误：{e}")
        finally:
            # 关闭浏览器
            browser.close()

def process_pdf_to_png(file_path, prompt_path, output_dir):
    """
    封装处理PDF文件并生成PNG的逻辑
    :param file_path: 上传的PDF文件路径
    :param prompt_path: 提示词文件路径
    :param output_dir: 输出目录
    :return: 生成的PNG文件路径
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_html = os.path.join(output_dir, f"{timestamp}.html")
    output_png = os.path.join(output_dir, f"{timestamp}.png")
    
    response = invoke_with_attachment_qwen(file_path, prompt_path, "翻译成中文，并输出为HTML格式")
    save_html(response, output_html)
    save_note_pic(output_html, output_png)
    
    return output_png

# 示例调用代码
if __name__ == "__main__":

    file_path = "./storage/input/residential.pdf"
    prompt_path = "./static/prompts/keshihua0.prompt"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = f"./static/note_output/{timestamp}.html"  # 使用时间戳作为文件名
    output_pic_path = f"./static/note_output/{timestamp}.png"

    # response = invoke_with_attachment_qwen(file_path, prompt_path, "翻译成中文，并输出为HTML格式", MODEL_NAME="deepseek-v3")
    response = invoke_with_attachment_kimi(file_path, prompt_path, "使用中文")
    # model="Moonshot-Kimi-K2-Instruct",
    print(response)
    save_html(response, output_path)
    save_note_pic(output_path, output_pic_path)