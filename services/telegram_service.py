import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def build_products(order):
    text = ""

    for item in order.items.all():
        name = (
            item.product.product_name_uz
            or item.product.product_name_kz
            or item.product.product_name_ru
        )
        text += f"🍫 <b>{name}</b> × {item.quantity}\n"

    return text


def build_message(order):

    products = build_products(order)

    phone_clean = order.phone_number.replace("+", "")

    whatsapp_link = f"https://wa.me/{phone_clean}"

    message = f"""
<b>🛒 NEW ORDER #{order.id}</b>

━━━━━━━━━━━━━━

<b>👤 Customer</b>
{order.name} {order.surname}

<b>📞 Phone</b>
<a href="{whatsapp_link}">{order.phone_number}</a>

<b>🚚 Order type</b>
{order.order_type}

━━━━━━━━━━━━━━

<b>📦 Products</b>

{products}

━━━━━━━━━━━━━━

<b>💰 Total</b>
<b>{order.total_price} ₸</b>
"""

    return message


def send_order_to_telegram(order):

    message = build_message(order)

    url = f"{BASE_URL}/sendDocument"

    file_path = order.payment_check_file.path

    with open(file_path, "rb") as f:

        files = {
            "document": f
        }

        data = {
            "chat_id": CHAT_ID,
            "caption": message,
            "parse_mode": "HTML"
        }

        requests.post(url, data=data, files=files)