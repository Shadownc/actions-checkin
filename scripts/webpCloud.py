import os
import requests
import json
import re

def main():
    token = os.getenv('WEBPCLOUD_TOKEN')
    if not token:
        print("Error: WEBPCLOUD_TOKEN is not set.")
        return

    url = 'https://webppt.webp.se/v1/user/check_in'
    headers = {
        'Content-Type': 'application/json',
        'token': token,
        'User-Agent': 'Mozilla/5.0'
    }
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        
        if 'success' in response_json:
            if response_json['success']:
                # 签到成功
                message = response_json.get('data', '签到成功。')
                
                # 使用正则表达式提取永久额度的数字
                match = re.search(r'added permanent quota:\s*(\d+)', message)
                if match:
                    quota = match.group(1)
                    print(f"✅ 签到成功: 永久额度新增{quota}")
                else:
                    print(f"✅ 签到成功: {message}")
            else:
                # 已经签到过
                message = response_json.get('messages', '今天已经签到过了。')
                print(f"ℹ️ 已经签到过: {message}")
        else:
            # 未预料到的响应格式
            print("⚠️ 未知的响应格式:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
        try:
            error_content = response.json()
            print(f"错误详情: {json.dumps(error_content, indent=2, ensure_ascii=False)}")
            # 检查是否包含 "has checked in today"
            message = error_content.get('messages', '')
            if "has checked in today" in message:
                # 检查到用户已签到
                print("ℹ️ 已签到过: 今天已经签到过了。")
            else:
                # 打印其他错误详情
                print(f"错误详情: {json.dumps(error_content, indent=2, ensure_ascii=False)}")
        except ValueError:
            print(f"响应内容: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")

if __name__ == "__main__":
    main()
