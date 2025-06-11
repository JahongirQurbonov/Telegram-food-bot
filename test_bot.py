import asyncio
from bot.config import config
from aiogram import Bot

async def test_bot():
    """Botni test qilish"""
    print("🔍 Bot tokenini tekshirish...")
    
    if not config.BOT_TOKEN:
        print("❌ BOT_TOKEN topilmadi!")
        print("📝 .env faylida BOT_TOKEN ni tekshiring")
        return
    
    try:
        bot = Bot(token=config.BOT_TOKEN)
        me = await bot.get_me()
        
        print("✅ Bot muvaffaqiyatli ulandi!")
        print(f"🤖 Bot nomi: {me.first_name}")
        print(f"📝 Username: @{me.username}")
        print(f"🆔 Bot ID: {me.id}")
        print(f"🔗 Bot linki: https://t.me/{me.username}")
        
        await bot.session.close()
        
        print("\n🚀 Botni ishga tushirish uchun:")
        print("python run.py")
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        print("🔍 Bot tokenini tekshiring")

if __name__ == "__main__":
    asyncio.run(test_bot())
