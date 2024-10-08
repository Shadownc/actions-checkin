import sys
import os
import requests
import json
import re

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from dotenv import load_dotenv
from utils.qywechat_notify import send_wechat_notification
from utils.qmsg_notify import send_qmsg_notification
from utils.serve_chan_notify import send_server_chan_notification

# 仅在本地环境中加载 .env 文件
if os.getenv("GITHUB_ACTIONS") is None:  # GITHUB_ACTIONS 在 GitHub Actions 环境中会自动设置为 "true"
    load_dotenv()


def check_in_webp_cloud(token):
    """执行 WebP Cloud 签到请求并处理响应"""
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
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"⚠️ HTTP 错误发生: {http_err}")
        try:
            # 尝试获取并打印详细的错误信息
            error_content = response.json()
            print(f"❗错误详情: {json.dumps(error_content, indent=2, ensure_ascii=False)}")
            return error_content
        except ValueError:
            # 如果响应不是 JSON 格式，则直接打印文本
            print(f"❗响应内容: {response.text}")
            return None
    except requests.exceptions.RequestException as req_err:
        print(f"⚠️ 请求过程中发生错误: {req_err}")
        return None


def extract_quota(message):
    """使用正则表达式提取永久额度的数字"""
    match = re.search(r'added permanent quota:\s*(\d+)', message)
    if match:
        return match.group(1)
    return None


def process_check_in_response(response_json):
    """处理签到响应，根据不同的情况发送通知"""
    if response_json and 'success' in response_json:
        if response_json['success']:
            # 签到成功，提取消息
            message = response_json.get('data', '🎉 签到成功。')
            quota = extract_quota(message)
            if quota:
                print(f"✅ 签到成功: 永久额度新增 {quota}")
                return f"🎉 WebP Cloud 签到成功: 永久额度新增 {quota} 🚀"
            else:
                print(f"✅ 签到成功: {message}")
                return f"🎉 WebP Cloud 签到成功: {message} 🚀"
        else:
            # 已经签到过
            message = response_json.get('messages', '今天已经签到过了。')
            print(f"ℹ️ 已经签到过: {message}")
            return f"😨️ WebP Cloud: 今天已经签到过了。"
    else:
        # 未知的响应格式
        print("⚠️ 未知的响应格式:")
        print(json.dumps(response_json, indent=2, ensure_ascii=False))
        return "⚠️ WebP Cloud 签到时收到未知响应格式。"


def main():
    # 获取环境变量中的 WebP Cloud 签到令牌
    token = os.getenv('WEBPCLOUD_TOKEN')
    if not token:
        print("❌ Error: WEBPCLOUD_TOKEN is not set.")
        return

    # 执行签到请求
    response_json = check_in_webp_cloud(token)
    if response_json:
        # 处理签到响应并获取通知消息
        notification_message = process_check_in_response(response_json)
        if notification_message:
            # 发送企业微信通知
            send_wechat_notification(notification_message)
            send_qmsg_notification(notification_message)
            send_server_chan_notification('WebP Cloud', notification_message)


if __name__ == "__main__":
    main()
