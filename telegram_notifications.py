import requests
from constants import API_URL, MY_GROUP_ID


def send_telegram_message(message, chat_id=MY_GROUP_ID):
    base_url = f"{API_URL}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(base_url)
    print("Telegram notification sent")
