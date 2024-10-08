import os
import requests
from dotenv import load_dotenv

if os.getenv("GITHUB_ACTIONS") is None:
    load_dotenv()

def send_qmsg_notification(content):
    qmsg_key = os.getenv('QMSG_KEY')  # 从环境变量中获取 Qmsg 酱的 key

    # 检查 qmsg_key 是否为 None 或空字符串
    if not qmsg_key:
        print("⚠️ qmsg_key 未设置 请设置后重试！")
        return

    qmsg_url = f'https://qmsg.zendee.cn/jsend/{qmsg_key}'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "msg": content
    }

    try:
        response = requests.post(qmsg_url, headers=headers, json=data)
        response.raise_for_status()  # 如果响应状态码不是 200，抛出 HTTPError 异常
        print("✅ Qmsg酱通知发送成功。")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")