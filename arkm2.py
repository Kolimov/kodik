import hmac
import hashlib
import base64
import requests
import time

# Настройки API
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
BASE_URL = "https://arkm.com/api"
REQUEST_PATH = "/orders/cancel/all" 
METHOD = "POST"
BODY = "{}"

# Прокси-сервер(мое)
PROXY = ""
proxies = {
    "http": PROXY,
    "https": PROXY
}

api_secret_bytes = base64.b64decode(API_SECRET)


EXPIRES = (int(time.time()) + 300) * 1000000  

#подпись(тут проблема?)
message = f"{API_KEY}{EXPIRES}{METHOD}{REQUEST_PATH}{BODY}"

#HMAC
signature = hmac.new(api_secret_bytes, message.encode(), hashlib.sha256).digest()

#bs64
signature_base64 = base64.b64encode(signature).decode()

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Arkham-Api-Key": API_KEY,
    "Arkham-Expires": str(EXPIRES),
    "Arkham-Signature": signature_base64
}

#post
def ping_api():
    try:
        response = requests.post(f"{BASE_URL}{REQUEST_PATH}", json=BODY, headers=headers, proxies=proxies)

        if response.status_code == 200:
            print("Успешный запрос:", response.json())
        else:
            print(f"Ошибка при выполнении запроса: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")

#vizov
if __name__ == "__main__":
    ping_api()
