from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from bot.buttons import get_start_keyboard, get_main_menu_keyboard, get_menu_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    """Start buyrug'ini qayta ishlash"""
    user_name = message.from_user.first_name or "Foydalanuvchi"
    
    welcome_text = (
        f"Salom {user_name}! 🍟\n\n"
        "🍔 <b>Durger King</b> ga xush kelibsiz!\n"
        "Welcome to Durger King!\n\n"
        "Mazali va sog'lom fast food buyurtma qiling!\n"
        "Order delicious and healthy fast food!"
    )
    
    await message.answer(
        text=welcome_text,
        reply_markup=get_start_keyboard()
    )

@router.callback_query(F.data == "show_menu")
async def show_menu_handler(callback: CallbackQuery):
    """Menyu ko'rsatish"""
    menu_text = (
        "🍽️ <b>Bizning Menyu / Our Menu</b>\n\n"
        "🍔 Burger - $4.99\n"
        "🍟 Fries - $1.49\n"
        "🌭 Hotdog - $3.49\n"
        "🌮 Taco - $3.99\n"
        "🍕 Pizza - $7.99\n"
        "🥤 Coke - $1.49\n"
        "🍰 Cake - $4.99 (NEW!)\n"
        "🍦 Ice Cream - $5.99\n\n"
        "Buyurtma berish uchun mahsulotni tanlang!\n"
        "Select a product to order!"
    )
    
    await callback.message.edit_text(
        text=menu_text,
        reply_markup=get_menu_keyboard()
    )
    await callback.answer()

# Har bir mahsulot uchun handler
@router.callback_query(F.data.startswith("order_"))
async def order_handler(callback: CallbackQuery):
    """Buyurtma berish"""
    item = callback.data.replace("order_", "")
    
    # Mahsulot ma'lumotlari
    items = {
        "burger": {"name": "🍔 Burger", "price": 4.99},
        "fries": {"name": "🍟 Fries", "price": 1.49},
        "hotdog": {"name": "🌭 Hotdog", "price": 3.49},
        "taco": {"name": "🌮 Taco", "price": 3.99},
        "pizza": {"name": "🍕 Pizza", "price": 7.99},
        "coke": {"name": "🥤 Coke", "price": 1.49},
        "cake": {"name": "🍰 Cake", "price": 4.99},
        "icecream": {"name": "🍦 Ice Cream", "price": 5.99}
    }
    
    if item in items:
        product = items[item]
        order_text = (
            f"✅ <b>Buyurtma qabul qilindi!</b>\n"
            f"Order received!\n\n"
            f"📦 Mahsulot: {product['name']}\n"
            f"💰 Narx: ${product['price']:.2f}\n\n"
            f"🚚 Yetkazib berish vaqti: 25-30 daqiqa\n"
            f"Delivery time: 25-30 minutes\n\n"
            f"📞 Aloqa: +998 90 123 45 67\n"
            f"Contact: +998 90 123 45 67"
        )
        
        await callback.message.edit_text(
            text=order_text,
            reply_markup=get_main_menu_keyboard()
        )
        
        # Console'ga log
        print(f"📊 Yangi buyurtma: {callback.from_user.full_name} - {product['name']} - ${product['price']:.2f}")
    
    await callback.answer("Buyurtma qabul qilindi! ✅")

@router.callback_query(F.data == "contact")
async def contact_handler(callback: CallbackQuery):
    """Kontakt ma'lumotlari"""
    contact_text = (
        "📞 <b>Aloqa Ma'lumotlari / Contact Information</b>\n\n"
        "📧 Email: support@durgerking.com\n"
        "📱 Phone: +998 90 123 45 67\n"
        "🕒 Ish vaqti: 9:00 - 22:00\n"
        "🕒 Working hours: 9:00 - 22:00\n"
        "📍 Manzil: Toshkent, O'zbekiston\n"
        "📍 Address: Tashkent, Uzbekistan\n\n"
        "🚚 Bepul yetkazib berish 30 daqiqada!\n"
        "🚚 Free delivery in 30 minutes!"
    )
    
    await callback.message.edit_text(
        text=contact_text,
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "about")
async def about_handler(callback: CallbackQuery):
    """Bot haqida ma'lumot"""
    about_text = (
        "🍔 <b>Durger King Bot</b>\n\n"
        "Bu bot orqali siz eng mazali va sog'lom fast food buyurtma qilishingiz mumkin!\n\n"
        "Use this bot to order the most delicious and healthy fast food!\n\n"
        "✨ <b>Bizning afzalliklarimiz:</b>\n"
        "🚀 Tez yetkazib berish\n"
        "💯 Sifat kafolati\n"
        "🌟 Eng yaxshi narxlar\n"
        "🇺🇿 O'zbekistonda tayyorlangan\n\n"
        "✨ <b>Our advantages:</b>\n"
        "🚀 Fast delivery\n"
        "💯 Quality guarantee\n"
        "🌟 Best prices\n"
        "🇺🇿 Made in Uzbekistan"
    )
    
    await callback.message.edit_text(
        text=about_text,
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_start")
async def back_to_start_handler(callback: CallbackQuery):
    """Bosh sahifaga qaytish"""
    user_name = callback.from_user.first_name or "Foydalanuvchi"
    
    welcome_text = (
        f"Salom {user_name}! 🍟\n\n"
        "🍔 <b>Durger King</b> ga xush kelibsiz!\n"
        "Welcome to Durger King!\n\n"
        "Mazali va sog'lom fast food buyurtma qiling!\n"
        "Order delicious and healthy fast food!"
    )
    
    await callback.message.edit_text(
        text=welcome_text,
        reply_markup=get_start_keyboard()
    )
    await callback.answer()

@router.message()
async def echo_handler(message: Message):
    """Boshqa xabarlar uchun"""
    await message.answer(
        "🤖 Buyurtma berish uchun /start buyrug'ini yuboring!\n\n"
        "To place an order, send /start command!",
        reply_markup=get_start_keyboard()
    )
