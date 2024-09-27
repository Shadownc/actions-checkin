# scripts/check_in.py
import os
import requests

def main():
    token = os.getenv('WEBPCLOUD_TOKEN')
    url = 'https://webppt.webp.se/v1/user/check_in'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json',
        'Origin': 'https://dashboard.webp.se',
        'Priority': 'u=1, i',
        'Referer': 'https://dashboard.webp.se/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not)A;Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Check-in response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error during check-in: {e}")

if __name__ == "__main__":
    main()
