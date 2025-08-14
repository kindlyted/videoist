import os 
from pathlib import Path
from openai import OpenAI

# gpt part 生成正文，postist_core.py里也有，但后缀不同表示api不同
def generating_byds(content, prompt_path):
    client = OpenAI(
        api_key=os.getenv('API_KEY_DS'),
        base_url=os.getenv('URL_DS'), 
    )
    # 定义提示词
    with open(prompt_path, 'r', encoding='utf-8') as file:
        your_prompt = file.read()
    your_prompt = your_prompt + content
    try:
        completion = client.chat.completions.create(
            model='deepseek-chat',   
            messages = [
                {
                    "role": "user",
                    "content": your_prompt
                }
            ],
            stream=False
        )
        print(completion.choices[0].message.content)
        answer = completion.choices[0].message.content
    except Exception as e:
        print("提示", e)
        answer = "敏感词censored by Deepseek"
    print("DeepSeek大模型工作中，请稍等片刻")
    return answer

# gpt part 生成正文，postist_core.py里也有，但后缀不同表示api不同
def generating_bykm(content, prompt_path):
    client = OpenAI(
        api_key=os.getenv('API_KEY_KIMI'),
        base_url=os.getenv('URL_KIMI'), 
    )
    # 定义提示词
    with open(prompt_path, 'r', encoding='utf-8') as file:
        your_prompt = file.read()
    your_prompt = your_prompt + content
    try:
        completion = client.chat.completions.create(
            model='moonshot-v1-8k',   
            messages = [
                {
                    "role": "user",
                    "content": your_prompt
                }
            ],
            stream=False
        )
        print(completion.choices[0].message.content)
        answer = completion.choices[0].message.content
    except Exception as e:
        print("提示", e)
        answer = "敏感词censored by Moonshot"
    print("Moonshot大模型工作中，请稍等片刻")
    return answer

# gpt part 生成正文
def generating_jskb(content, prompt_path):
    client = OpenAI(
        api_key=os.getenv('API_KEY_DS'),
        base_url=os.getenv('URL_DS'), 
    )
    # 定义提示词
    with open(prompt_path, 'r', encoding='utf-8') as file:
        your_prompt = file.read()
    # your_prompt = your_prompt + content
    try:
        completion = client.chat.completions.create(
            model='deepseek-chat',   
            messages = [{"role": "system", "content": your_prompt}, {"role": "user", "content": content}],
            stream=False,
            temperature=0.4,          # 降低随机性
            # max_tokens=4096,          # 防止过长
            top_p=0.9,                # 平衡多样性
            frequency_penalty=0.5,    # 减少重复
            presence_penalty=0.3,     # 适度控制主题跳跃
            response_format={'type': 'json_object'}
        )
        answer = completion.choices[0].message.content
    except Exception as e:
        print("提示", e)
        answer = "敏感词censored by Deepseek"
    print("DeepSeek大模型工作中，请稍等片刻")
    return answer

# gpt part 生成正文
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
