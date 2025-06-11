import asyncio
import logging
from bot.main import main

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("🚀 Botni local da ishga tushirish...")
    print("⏹️  To'xtatish uchun Ctrl+C bosing")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Bot to'xtatildi")
    except Exception as e:
        print(f"❌ Xatolik: {e}")
