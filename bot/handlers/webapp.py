import json
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    """WebApp'dan kelgan ma'lumotlarni qayta ishlash"""
    try:
        # WebApp'dan kelgan JSON ma'lumotlarni parse qilish
        print(f"Received web_app_data: {message.web_app_data.data}")
        data = json.loads(message.web_app_data.data)
        
        # Buyurtma ma'lumotlarini olish
        cart_items = data.get('cart', [])
        total_price = data.get('total', 0)
        comment = data.get('comment', '')
        
        # Buyurtma tasdiqini yaratish
        order_text = "✅ <b>Buyurtmangiz qabul qilindi!</b>\n"
        order_text += "Your order has been received!\n\n"
        order_text += "📋 <b>Buyurtma tafsilotlari / Order details:</b>\n"
        
        for item in cart_items:
            item_total = item['price'] * item['quantity']
            order_text += f"• {item['name']} x{item['quantity']} - ${item_total:.2f}\n"
        
        if comment:
            order_text += f"\n💬 <b>Izoh / Comment:</b> {comment}\n"
        
        order_text += f"\n💰 <b>Jami / Total:</b> ${total_price:.2f}\n"
        order_text += "\n🚚 <b>Yetkazib berish vaqti:</b> 25-30 daqiqa"
        order_text += "\n🚚 <b>Estimated delivery:</b> 25-30 minutes"
        order_text += "\n\n📞 Aloqa uchun: +998 90 123 45 67"
        
        await message.answer(order_text)
        
        # Admin uchun xabar (ixtiyoriy)
        admin_text = f"🔔 <b>Yangi buyurtma!</b>\n\n"
        admin_text += f"👤 Mijoz: {message.from_user.full_name}\n"
        admin_text += f"🆔 User ID: {message.from_user.id}\n"
        admin_text += f"💰 Summa: ${total_price:.2f}\n"
        admin_text += f"📝 Mahsulotlar: {len(cart_items)} ta"
        
        print(f"📊 Admin log: {admin_text}")  # Console'ga chiqarish
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        await message.answer(
            "❌ Buyurtmani qayta ishlashda xatolik yuz berdi.\n"
            "Error processing your order. Please try again."
        )
    except Exception as e:
        print(f"❌ WebApp xatoligi: {e}")
        await message.answer(
            "❌ Nimadir noto'g'ri ketdi. Qo'llab-quvvatlash bilan bog'laning.\n"
            "Something went wrong. Please contact support."
        )
