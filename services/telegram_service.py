import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def build_products(order):
    products_text = ""

    for item in order.items.all():
        products_text += f"• {item.product.product_name} × {item.quantity}\n"

    return products_text


def build_message(order):
    products = build_products(order)

    message = f"""
<b>🛒 NEW ORDER #{order.id}</b>

<b>👤 Customer</b>
{order.name} {order.surname}

<b>📞 Phone</b>
{order.phone_number}

<b>🚚 Order type</b>
{order.order_type}

<b>📦 Products</b>
{products}

<b>💰 Total price</b>
{order.total_price} ₸

<b>💳 Payment check attached below</b>
"""

    return message


async def send_order_to_telegram(order):
    message = build_message(order)

    url = f"{BASE_URL}/sendDocument"

    file_path = order.payment_check_file.path

    async with aiohttp.ClientSession() as session:

        with open(file_path, "rb") as f:

            data = aiohttp.FormData()
            data.add_field("chat_id", CHAT_ID)
            data.add_field("caption", message)
            data.add_field("parse_mode", "HTML")
            data.add_field(
                "document",
                f,
                filename="payment_check.jpg",
                content_type="application/octet-stream"
            )

            await session.post(url, data=data)