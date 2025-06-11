import subprocess
import sys

def install_requirements():
    """Kutubxonalarni o'rnatish"""
    requirements = [
        "aiogram==3.13.1",
        "aiohttp==3.9.1", 
        "python-dotenv==1.0.0"
    ]
    
    print("📦 Kutubxonalarni o'rnatish...")
    
    for requirement in requirements:
        try:
            print(f"⬇️ O'rnatilmoqda: {requirement}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f"✅ O'rnatildi: {requirement}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Xatolik: {requirement} - {e}")
    
    print("🎉 Barcha kutubxonalar o'rnatildi!")

if __name__ == "__main__":
    install_requirements()
