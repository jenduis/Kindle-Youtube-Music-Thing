import requests
import time

# Update these to whatever you like
APP_ID = "kindle_dashboard"
APP_NAME = "Kindle Music Display"
APP_VERSION = "1.0.0"
BASE_URL = "http://localhost:9863/api/v1"

def get_token():
    # 1. Request a code
    print("Requesting auth code...")
    res = requests.post(f"{BASE_URL}/auth/requestcode", json={
        "appId": APP_ID,
        "appName": APP_NAME,
        "appVersion": APP_VERSION
    })
    code = res.json().get('code')
    print(f"Got code: {code}. PLEASE CLICK 'ALLOW' IN YTM DESKTOP NOW!")

    # 2. Wait for user to click "Allow" in the YTM App
    # This request will hang for up to 30 seconds waiting for you
    try:
        token_res = requests.post(f"{BASE_URL}/auth/request", json={
            "appId": APP_ID,
            "code": code
        }, timeout=35)
        token = token_res.json().get('token')
        print(f"SUCCESS! YOUR TOKEN IS: {token}")
        return token
    except:
        print("Timed out or denied. Make sure you click 'Allow' in the app.")
        return None

if __name__ == "__main__":
    get_token()