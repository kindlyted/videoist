import os
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from openai import OpenAI
from playwright.sync_api import sync_playwright

def invoke_with_attachment_kimi(file_path, prompt_path, user_input, MODEL_NAME="kimi-k2-0711-preview"):
    client = OpenAI(
        api_key=os.getenv('API_KEY_KIMI'),
        base_url=os.getenv('URL_KIMI'), 
    )
    
    # 读取系统提示
    with open(prompt_path, 'r', encoding='utf-8') as file:
        system_prompt = file.read()
    
    # 上传文件并获取内容
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    file_content = client.files.content(file_id=file_object.id).text

    try:
        # 进行聊天
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": file_content}, # 这里和Qwen不同，Kimi直接使用文件内容
                {"role": "user", "content": user_input},
            ],
            temperature=0.6,
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        print(e)
        answer = "敏感词censored by Moonshot"
    
    # 清理文件
    try:
        file_list = client.files.list()
        print(file_list)
        for file in file_list.data:
            client.files.delete(file_id=file.id)
        print("已清理所有文件。")
    except Exception as e:
        print(f"清理文件时出错: {e}")
    
    return answer

def invoke_with_attachment_qwen(file_path, prompt_path, user_input, MODEL_NAME="qwen-long"):
    client = OpenAI(
        api_key=os.getenv('API_KEY_QWEN'),
        base_url=os.getenv('URL_QWEN'), 
    )
    
    # 读取系统提示
    with open(prompt_path, 'r', encoding='utf-8') as file:
        system_prompt = file.read()
    
    # 上传文件
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    print(file_object.id)  # 打印文件对象信息，确认是否正确
    print(file_object.model_dump_json())

    try:
        # 进行聊天
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": f'fileid://{file_object.id}'}, # Qwen使用fileid://格式引用文件
                {"role": "user", "content": user_input},
            ],
            temperature=0.6,
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        print(e)
        answer = "敏感词censored by QWEN"
    
    # 清理文件
    try:
        file_list = client.files.list()
        print(file_list)
        for file in file_list.data:
            client.files.delete(file_id=file.id)
        print("已清理所有文件。")
    except Exception as e:
        print(f"清理文件时出错: {e}")
    
    return answer

# Qwen大模型调用
def invoke_qwen(prompt_path, user_input, MODEL_NAME='deepseek-v3'):
    client = OpenAI(
        api_key=os.getenv('API_KEY_QWEN'),
        base_url=os.getenv('URL_QWEN'), 
    )
    print("大模型工作中，请稍等片刻")
    with open(prompt_path, 'r', encoding='utf-8') as file:
        system_prompt = file.read()
    print("系统提示词长度:", len(system_prompt))

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,   
            messages=[
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": user_input}
            ],
            stream=False,
            # max_tokens=4096,  # 设置最大token数
            temperature=0.6
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        print("提示", e)
        answer = "敏感词censored by QWEN"

    return answer

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

    file_path = "./note/static/input/residential.pdf"
    prompt_path = "./note/static/prompts/keshihua0.prompt"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = f"./note/static/output/{timestamp}.html"  # 使用时间戳作为文件名
    output_pic_path = f"./note/static/output/{timestamp}.png"

    # response = invoke_with_attachment_qwen(file_path, prompt_path, "翻译成中文，并输出为HTML格式", MODEL_NAME="deepseek-v3")
    response = invoke_with_attachment_kimi(file_path, prompt_path, "使用中文")
    # model="Moonshot-Kimi-K2-Instruct",
    print(response)
    save_html(response, output_path)
    save_note_pic(output_path, output_pic_path)