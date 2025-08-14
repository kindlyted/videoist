import requests
import json

# 假设Flask应用运行在本地5010端口
base_url = "http://localhost:5010"

# 测试获取平台统计数据
def test_platform_stats():
    # 使用假设的token
    token = "test_token"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{base_url}/api/platform-stats", headers=headers)
    
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"错误响应: {response.text}")

if __name__ == "__main__":
    print("测试API响应...")
    test_platform_stats()