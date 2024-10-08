import os
import requests
from dotenv import load_dotenv

if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv()

def send_server_chan_notification(title, desp, channel=9):
    server_chan_key = os.getenv('SERVER_CHAN_KEY')
    server_chan_url = f'https://sctapi.ftqq.com/{server_chan_key}.send'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    data = {
        'title': title,
        'desp': desp,
        'channel': channel
    }

    try:
        response = requests.post(server_chan_url, headers=headers, data=data)
        response.raise_for_status()
        print("✅ Server酱通知发送成功。")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")
