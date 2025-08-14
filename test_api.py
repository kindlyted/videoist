import requests
import json

# 测试后端API连接
def test_api_connection():
    url = "http://localhost:5010/login"
    payload = {
        "username": "admin",
        "password": "123456"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code, response.text
    except Exception as e:
        print(f"Error connecting to API: {str(e)}")
        return None, str(e)

if __name__ == "__main__":
    print("Testing API connection...")
    test_api_connection()