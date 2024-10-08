import sys
import os
import requests
import json

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.qywechat_notify import send_wechat_notification  # 假设你有此函数实现企业微信通知
from utils.qmsg_notify import send_qmsg_notification
from utils.serve_chan_notify import send_server_chan_notification


def load_env_variables():
    """加载并返回环境变量。"""
    # 如果不在 GitHub Actions 环境中，加载 .env 文件
    if os.getenv("GITHUB_ACTIONS") is None:
        load_dotenv()

    # 从环境变量中获取 csrfToken 和 cookie
    csrfToken = os.getenv("FOLLOW_CSRF_TOKEN")
    cookie = os.getenv("FOLLOW_COOKIE")

    if not csrfToken or not cookie:
        raise ValueError("缺少必须的环境变量：CSRF Token 或 Cookie")

    return csrfToken, cookie


def sign_in():
    csrfToken, cookie = load_env_variables()
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

    # 发送 POST 请求
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # 解析返回结果
    result = response.json()
    code = result.get('code')
    message = result.get('message', 'No message')

    # 处理返回结果，并推送通知
    if code == 0:
        print("签到成功")
        send_wechat_notification("follow签到状态：🎉✨签到成功")
        send_qmsg_notification("follow签到状态：🎉✨签到成功")
        send_server_chan_notification('follow', "follow签到状态：🎉✨签到成功")
    else:
        if "Already claimed" in message:
            print("今日已签到")
            send_wechat_notification("follow签到状态：😨今日已签到")
            send_qmsg_notification("follow签到状态：😨今日已签到")
            send_server_chan_notification('follow', "follow签到状态：😨今日已签到")
        else:
            error_message = f"签到失败: {message}"
            print(error_message)
            send_wechat_notification(error_message)
            send_qmsg_notification(error_message)
            send_server_chan_notification('follow', error_message)


if __name__ == "__main__":
    sign_in()
