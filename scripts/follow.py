import requests
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from dotenv import load_dotenv
from utils.qywechat_notify import send_wechat_notification


def load_env_variables():
    """加载并返回环境变量。"""
    if os.getenv("GITHUB_ACTIONS") is None:  # 如果不在 GitHub Actions 环境中，加载 .env 文件
        load_dotenv()

    csrfToken = os.getenv("FOLLOW_CSRF_TOKEN")
    cookie = os.getenv("FOLLOW_COOKIE")

    if not csrfToken or not cookie:
        raise ValueError("缺少必须的环境变量：CSRF Token 或 Cookie")

    return csrfToken, cookie


def send_sign_in_request(csrfToken, cookie):
    """发送签到请求到 API。"""
    url = "https://api.follow.is/wallets/transactions/claim_daily"

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/4G Language/zh_CN',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Cookie': cookie
    }

    payload = {
        "csrfToken": csrfToken
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()  # 如果响应状态码不是 200，抛出 HTTPError 异常
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"请求失败: {e}")


def handle_sign_in_result(result):
    """处理签到请求的返回结果。"""
    code = result.get('code')
    message = result.get('message', '无消息')

    if code == 0:
        print("签到成功")
        send_wechat_notification("follow签到状态：🎉✨签到成功")
    else:
        if "Already claimed" in message:
            print("今日已签到")
            send_wechat_notification("follow签到状态：😨今日已签到")
        else:
            error_message = f"签到失败: {message}"
            print(error_message)
            send_wechat_notification(error_message)


def sign_in():
    """执行签到的主函数。"""
    try:
        csrfToken, cookie = load_env_variables()
        result = send_sign_in_request(csrfToken, cookie)
        handle_sign_in_result(result)
    except ValueError as e:
        print(f"错误: {e}")
        send_wechat_notification(f"follow签到失败，缺少环境变量: {e}")
    except RuntimeError as e:
        print(f"错误: {e}")
        send_wechat_notification(f"follow签到失败，请求错误: {e}")


if __name__ == "__main__":
    sign_in()
