import asyncio
import logging
import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config
from bot.handlers import start, webapp

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Botni ishga tushirish"""
    # Bot tokenini tekshirish
    if not config.BOT_TOKEN:
        logger.error("❌ BOT_TOKEN topilmadi!")
        logger.error("📝 .env faylida BOT_TOKEN ni tekshiring")
        return
    
    logger.info(f"✅ Bot token topildi!")
    
    try:
        # Bot va Dispatcher yaratish
        bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher()
        
        # Handlerlarni ro'yxatdan o'tkazish
        dp.include_router(start.router)
        dp.include_router(webapp.router)
        
        # Bot ma'lumotlarini olish
        me = await bot.get_me()
        logger.info(f"🤖 Bot: @{me.username} ({me.first_name})")
        logger.info(f"🆔 Bot ID: {me.id}")
        
        # Botni ishga tushirish
        logger.info("🚀 Bot ishga tushdi!")
        logger.info("💬 Telegram'da /start yuboring")
        logger.info("⏹️ To'xtatish uchun Ctrl+C bosing")
        
        # Polling boshlash
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Bot xatoligi: {e}")
    finally:
        if 'bot' in locals():
            await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Bot to'xtatildi")
    except Exception as e:
        print(f"❌ Umumiy xatolik: {e}")
