import logging
from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.exceptions import TelegramBadRequest
from bot.config import config

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.web_app_data)
async def handle_webapp_payment(message: Message):
    """WebApp'dan kelgan to'lov ma'lumotlarini qayta ishlash"""
    try:
        import json
        data = json.loads(message.web_app_data.data)
        
        cart_items = data.get('cart', [])
        total_price = data.get('total', 0)
        comment = data.get('comment', '')
        
        logger.info(f"💰 Payment request: ${total_price} from user {message.from_user.id}")
        
        # To'lov tokenini tekshirish
        if not config.PAYMENT_TOKEN:
            await message.answer(
                "❌ To'lov tizimi hozircha mavjud emas.\n"
                "Payment system is currently unavailable."
            )
            return
        
        # Invoice yaratish
        prices = []
        description_parts = []
        
        for item in cart_items:
            # Har bir mahsulot uchun narx (tiyin/kopeck da)
            item_price = int(item['price'] * item['quantity'] * 100)  # USD to cents
            prices.append(LabeledPrice(
                label=f"{item['emoji']} {item['name']} x{item['quantity']}", 
                amount=item_price
            ))
            description_parts.append(f"{item['name']} x{item['quantity']}")
        
        # Invoice ma'lumotlari
        title = "🍔 Durger King Order"
        description = f"Order: {', '.join(description_parts)}"
        payload = f"order_{message.from_user.id}_{message.message_id}"
        currency = "USD"
        
        # Invoice yuborish
        await message.answer_invoice(
            title=title,
            description=description,
            payload=payload,
            provider_token=config.PAYMENT_TOKEN,
            currency=currency,
            prices=prices,
            need_name=True,
            need_phone_number=True,
            need_email=False,
            need_shipping_address=True,
            send_phone_number_to_provider=True,
            send_email_to_provider=False,
            is_flexible=False,
            disable_notification=False,
            protect_content=False,
            reply_to_message_id=None,
            allow_sending_without_reply=True
        )
        
        logger.info(f"✅ Invoice sent successfully to user {message.from_user.id}")
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON decode error: {e}")
        await message.answer("❌ Ma'lumotlarni qayta ishlashda xatolik yuz berdi.")
    except TelegramBadRequest as e:
        logger.error(f"❌ Telegram API error: {e}")
        await message.answer("❌ To'lov tizimida xatolik yuz berdi. Keyinroq urinib ko'ring.")
    except Exception as e:
        logger.error(f"❌ Payment error: {e}")
        await message.answer("❌ To'lov jarayonida xatolik yuz berdi.")

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """To'lovdan oldin tekshirish"""
    logger.info(f"💳 Pre-checkout query from user {pre_checkout_query.from_user.id}")
    logger.info(f"💰 Amount: {pre_checkout_query.total_amount}")
    logger.info(f"📦 Payload: {pre_checkout_query.invoice_payload}")
    
    # To'lovni tasdiqlash
    await pre_checkout_query.answer(ok=True)
    logger.info("✅ Pre-checkout approved")

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    """Muvaffaqiyatli to'lov"""
    payment = message.successful_payment
    
    logger.info(f"🎉 Successful payment from user {message.from_user.id}")
    logger.info(f"💰 Amount: {payment.total_amount}")
    logger.info(f"💳 Currency: {payment.currency}")
    logger.info(f"📦 Payload: {payment.invoice_payload}")
    
    # Muvaffaqiyatli to'lov xabari
    success_text = (
        "🎉 <b>To'lov muvaffaqiyatli amalga oshirildi!</b>\n"
        "Payment successful!\n\n"
        f"💰 <b>Summa:</b> {payment.total_amount / 100:.2f} {payment.currency}\n"
        f"💳 <b>To'lov ID:</b> {payment.provider_payment_charge_id}\n\n"
        "🚚 <b>Buyurtmangiz tayyorlanmoqda!</b>\n"
        "Your order is being prepared!\n\n"
        "📞 Aloqa: +998 90 123 45 67\n"
        "🕒 Yetkazib berish: 25-30 daqiqa"
    )
    
    await message.answer(success_text)
    
    # Admin uchun xabar
    admin_text = (
        f"💰 <b>Yangi to'lov!</b>\n\n"
        f"👤 Mijoz: {message.from_user.full_name}\n"
        f"🆔 User ID: {message.from_user.id}\n"
        f"💰 Summa: {payment.total_amount / 100:.2f} {payment.currency}\n"
        f"💳 Provider ID: {payment.provider_payment_charge_id}\n"
        f"📦 Payload: {payment.invoice_payload}"
    )
    
    logger.info(f"📊 Admin notification: {admin_text}")
