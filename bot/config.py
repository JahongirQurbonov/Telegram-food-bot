import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

class Config:
    # Bot sozlamalari
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # WebApp sozlamalari  
    WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-webapp-url.com')
    
    # To'lov sozlamalari
    PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')  # Stripe/PaymentProvider token
    
    # Webhook sozlamalari (production uchun)
    WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
    WEBHOOK_PATH = f'/webhook' if BOT_TOKEN else None
    WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}' if WEBHOOK_HOST else None
    
    # Server sozlamalari
    WEBAPP_HOST = '0.0.0.0'
    WEBAPP_PORT = int(os.getenv('PORT', 8000))

# Config obyektini yaratish
config = Config()
