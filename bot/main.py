import asyncio
import logging
import sys
import os

# Loyiha yo'lini qo'shish
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        logger.error("❌ BOT_TOKEN topilmadi! .env faylini tekshiring")
        return
    
    # Bot va Dispatcher yaratish
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Handlerlarni ro'yxatdan o'tkazish
    dp.include_router(start.router)
    dp.include_router(webapp.router)
    
    # Botni ishga tushirish
    logger.info("🚀 Bot ishga tushmoqda...")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Bot xatoligi: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Bot to'xtatildi")
