import os
import requests
import dashscope

def qwen_speaking(OUTPUT_FILE: str, TEXT: str, VOICE: str, MODEL: str) -> None:
    """
    使用阿里云dashscope的qwen-tts模型进行语音合成并保存音频文件（同步版本）
    
    参数:
        OUTPUT_FILE: 输出音频文件路径
        TEXT: 要合成的文本内容
        VOICE: 语音角色，默认为"Cherry" Chelsie（女）Cherry（女）Ethan（男）Serena（女）
        MODEL: 使用的模型，默认为"qwen-tts"  qwen-tts-2025-05-22 与 qwen-tts-latest 还支持以下三种音色：Dylan（北京话-男）Jada（吴语-女）Sunny（四川话-女）
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    

    
    # 调用语音合成API
    response = dashscope.audio.qwen_tts.SpeechSynthesizer.call(
        model=MODEL,
        text=TEXT,
        voice=VOICE,
    )
    
    # 获取音频URL
    audio_url = response.output.audio["url"]
    
    # 下载并保存音频文件
    try:
        audio_response = requests.get(audio_url)
        audio_response.raise_for_status()  # 检查请求是否成功
        with open(OUTPUT_FILE, 'wb') as f:
            f.write(audio_response.content)
        print(f"音频文件已保存至：{OUTPUT_FILE}")
    except Exception as e:
        print(f"下载失败：{str(e)}")
        raise

if __name__ == "__main__":
    # 示例调用
    output_file = "./video/static/output/audio.mp3"
    with open('video/static/output/txt/20250615101246.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    voice = "Dylan"  # 可选，默认为"Cherry"
    
    try:
        qwen_speaking(output_file, text, voice, "qwen-tts-latest")
    except Exception as e:
        print(f"发生错误：{str(e)}")