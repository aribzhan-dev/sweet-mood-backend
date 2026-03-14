import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_order_to_telegram(order):

    message = f"""
🛒 Новый заказ

Имя: {order.name}
Фамилия: {order.surname}
Телефон: {order.phone_number}
"Локация": {order.location}
Тип заказа: {order.order_type}

Сумма: {order.total_price}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )