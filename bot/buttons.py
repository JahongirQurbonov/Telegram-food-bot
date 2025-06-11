from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from bot.config import config

def get_start_keyboard():
    """Start buyrug'i uchun tugmalar"""
    # Agar WebApp URL HTTPS bo'lsa, WebApp tugmasini ko'rsatish
    if config.WEBAPP_URL and config.WEBAPP_URL.startswith('https://'):
        print(f"Using WebApp URL: {config.WEBAPP_URL}")  # Debug uchun
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🍔 Order Food",
                        web_app=WebAppInfo(url=config.WEBAPP_URL)
                    )
                ]
            ]
        )
    else:
        # Vaqtincha oddiy tugmalar
        print(f"Invalid WebApp URL: {config.WEBAPP_URL}")  # Debug uchun
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🍔 Menu Ko'rish", 
                        callback_data="show_menu"
                    )
                ],
                [
                    InlineKeyboardButton(text="📞 Contact", callback_data="contact"),
                    InlineKeyboardButton(text="ℹ️ About", callback_data="about")
                ]
            ]
        )
    return keyboard

def get_main_menu_keyboard():
    """Asosiy menyu tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍔 Menu Ko'rish", 
                    callback_data="show_menu"
                )
            ],
            [
                InlineKeyboardButton(text="📞 Contact", callback_data="contact"),
                InlineKeyboardButton(text="ℹ️ About", callback_data="about")
            ],
            [
                InlineKeyboardButton(text="🔙 Back", callback_data="back_to_start")
            ]
        ]
    )
    return keyboard

def get_menu_keyboard():
    """Ovqat menyu tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🍔 Burger - $4.99", callback_data="order_burger"),
                InlineKeyboardButton(text="🍟 Fries - $1.49", callback_data="order_fries")
            ],
            [
                InlineKeyboardButton(text="🌭 Hotdog - $3.49", callback_data="order_hotdog"),
                InlineKeyboardButton(text="🌮 Taco - $3.99", callback_data="order_taco")
            ],
            [
                InlineKeyboardButton(text="🍕 Pizza - $7.99", callback_data="order_pizza"),
                InlineKeyboardButton(text="🥤 Coke - $1.49", callback_data="order_coke")
            ],
            [
                InlineKeyboardButton(text="🍰 Cake - $4.99", callback_data="order_cake"),
                InlineKeyboardButton(text="🍦 Ice Cream - $5.99", callback_data="order_icecream")
            ],
            [
                InlineKeyboardButton(text="🔙 Back", callback_data="back_to_start")
            ]
        ]
    )
    return keyboard
