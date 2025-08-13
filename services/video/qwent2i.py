import os
from http import HTTPStatus
import requests
from dashscope import ImageSynthesis #dashscope不需要显式传递apikey

def generate_image_qwen(input_prompt, file_path, MODEL_NAME="wan2.2-t2i-flash", aspect_ratio=1):
    # def getting_picture(query, dir, filename, aspect_ratio):
    # 初始调用
    # 根据比例设置宽高
    if aspect_ratio == 1:
        size = '768*512'
    elif aspect_ratio == 2:
        size = '512*768'
    elif aspect_ratio == 3:
        size = '1024*1024'
    else:
        print(f"⚠️ 未知比例参数 {aspect_ratio}，使用默认 768x512")
        size = '768*512'

    response = ImageSynthesis.call(
        model=MODEL_NAME,
        prompt=input_prompt,
        n=1,
        size=size
    )
    
    # 首先检查HTTP状态码
    if response.status_code != HTTPStatus.OK:
        print(f'Initial call failed, status_code: {response.status_code}, code: {response.code}, message: {response.message}')
        return False
    
    # 然后检查任务状态
    if hasattr(response, 'output') and hasattr(response.output, 'task_status'):
        if response.output.task_status == "FAILED":
            print(f'Task failed: {response.output.message}')
            return False
    
    # 确保有有效的结果
    if not hasattr(response, 'output') or not hasattr(response.output, 'results') or not response.output.results:
        print('No valid results in response')
        return False
    
    try:
        # 保存文件到指定路径
        for result in response.output.results:
            if not hasattr(result, 'url'):
                continue
            image_data = requests.get(result.url).content
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(image_data)
        print(f"Image successfully saved to: {file_path}")
        return True
    except Exception as e:
        print(f"Failed to save image: {str(e)}")
        return False

def generate_image_qwen_async(input_prompt, file_path, MODEL_NAME="wan2.2-t2i-flash", aspect_ratio=1):
    # 根据比例设置宽高
    if aspect_ratio == 1:
        size = '768*512'
    elif aspect_ratio == 2:
        size = '512*768'
    elif aspect_ratio == 3:
        size = '1024*1024'
    else:
        print(f"⚠️ 未知比例参数 {aspect_ratio}，使用默认 768x512")
        size = '768*512'

    # 初始异步调用
    response = ImageSynthesis.async_call(
        model=MODEL_NAME,
        prompt=input_prompt,
        n=1,
        size=size
    )
    
    # 首先检查HTTP状态码
    if response.status_code != HTTPStatus.OK:
        print(f'Initial call failed, status_code: {response.status_code}, code: {response.code}, message: {response.message}')
        return False
    
    print("Initial call successful, task submitted.")
    print(f"Task ID: {response.output.task_id}")
    print(response.usage)
    
    # 然后检查任务状态
    status = ImageSynthesis.fetch(response)
    if status.status_code != HTTPStatus.OK:
        print(f'Failed to fetch task status, status_code: {status.status_code}, '
              f'code: {status.code}, message: {status.message}')
        return False
    
    print(f"Task status: {status.output.task_status}")
    
    # 等待任务完成
    final_response = ImageSynthesis.wait(response)
    if final_response.status_code != HTTPStatus.OK:
        print(f'Failed to wait for task completion, status_code: {final_response.status_code}, '
              f'code: {final_response.code}, message: {final_response.message}')
        return False
    
    # 检查最终任务状态
    if hasattr(final_response.output, 'task_status') and final_response.output.task_status != "SUCCEEDED":
        print(f'Task failed with status: {final_response.output.task_status}, '
              f'message: {getattr(final_response.output, "message", "No error message")}')
        return False
    
    # 验证结果
    if not hasattr(final_response.output, 'results') or not final_response.output.results:
        print('No valid results in final response')
        return False
    
    # 保存图像
    try:
        # 保存文件到指定路径
        for result in final_response.output.results:
            if not hasattr(result, 'url'):
                continue
            image_data = requests.get(result.url).content
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(image_data)
        
        print(f"Image successfully saved to: {file_path}")
        return True
    except Exception as e:
        print(f"Failed to save image: {str(e)}")
        return False

if __name__ == '__main__':
    model = "flux-schnell"
    prompt = "a beautiful landscape with mountains and a river, high resolution, detailed"
    file_path = "./note/static/output/output_image.png"
    
    success = generate_image_qwen(prompt, file_path, model, aspect_ratio=1)

    success = generate_image_qwen_async(prompt, file_path, model, aspect_ratio=1)
    # if not success:
    #     print("second image generation failed")
