import os
import requests
from dotenv import load_dotenv

if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv()

def send_server_chan_notification(title, desp):
    server_chan_key = os.getenv('SERVER_CHAN_KEY')

    # 根据 server_chan_key 的前缀决定使用不同的推送URL
    if server_chan_key.startswith('sctp'):
        server_chan_url = f'https://{server_chan_key}.push.ft07.com/send'
    else:
        server_chan_url = f'https://sctapi.ftqq.com/{server_chan_key}.send'
    
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }

    data = {
        'title': title,
        'desp': desp
    }

    try:
        response = requests.post(server_chan_url, json=data, headers=headers)
        response.raise_for_status()
        print("✅ Server酱通知发送成功。")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")
