# scripts/check_in.py
import os
import requests
import json

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
        print(f"Check-in response: {response.json()}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        try:
            error_content = response.json()
            print(f"Error details: {json.dumps(error_content, indent=2, ensure_ascii=False)}")
        except ValueError:
            print(f"Response content: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error during check-in: {e}")

if __name__ == "__main__":
        main()
