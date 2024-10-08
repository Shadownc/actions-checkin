import os
import requests
from dotenv import load_dotenv

if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv()

def send_server_chan_notification(title, desp):
    server_chan_key = os.getenv('SERVER_CHAN_KEY')
    channel = os.getenv('SERVER_CHAN_CHANNEL', '9')  # 从环境变量读取channel 默认为9

    # 检查 server_chan_key 是否为 None 或空字符串
    if not server_chan_key:
        print("⚠️ SERVER_CHAN_KEY 未设置 请设置后重试！")
        return
    
    data = {
        'title': title,
        'desp': desp
    }

    # 根据 server_chan_key 的前缀决定使用不同的推送URL
    if server_chan_key.startswith('sctp'):
        server_chan_url = f'https://{server_chan_key}.push.ft07.com/send'
    else:
        server_chan_url = f'https://sctapi.ftqq.com/{server_chan_key}.send'
        data['channel'] = channel  # 推送通道 默认9
    
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }

    try:
        response = requests.post(server_chan_url, json=data, headers=headers)
        response.raise_for_status()
        print("✅ Server酱通知发送成功。")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")
