import os
import subprocess
import sys

def deploy_webapp():
    """WebApp'ni Vercel'ga deploy qilish"""
    print("📤 WebApp'ni deploy qilish...")
    
    try:
        # Vercel CLI mavjudligini tekshirish
        subprocess.run(["vercel", "--version"], check=True, capture_output=True)
        
        # Deploy qilish
        os.chdir("webapp")
        result = subprocess.run(["vercel", "--prod"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ WebApp muvaffaqiyatli deploy qilindi!")
            # URL ni olish
            lines = result.stdout.split('\n')
            for line in lines:
                if 'https://' in line and 'vercel.app' in line:
                    webapp_url = line.strip()
                    print(f"🌐 WebApp URL: {webapp_url}")
                    
                    # .env faylni yangilash
                    update_env_file(webapp_url)
                    break
        else:
            print(f"❌ Deploy xatoligi: {result.stderr}")
            
    except subprocess.CalledProcessError:
        print("❌ Vercel CLI topilmadi!")
        print("📝 O'rnatish: npm i -g vercel")
    except Exception as e:
        print(f"❌ Xatolik: {e}")

def update_env_file(webapp_url):
    """Environment faylini yangilash"""
    try:
        with open('../.env', 'r') as f:
            content = f.read()
        
        # WEBAPP_URL ni yangilash
        lines = content.split('\n')
        updated_lines = []
        webapp_updated = False
        
        for line in lines:
            if line.startswith('WEBAPP_URL='):
                updated_lines.append(f'WEBAPP_URL={webapp_url}')
                webapp_updated = True
            else:
                updated_lines.append(line)
        
        # Agar WEBAPP_URL yo'q bo'lsa, qo'shish
        if not webapp_updated:
            updated_lines.append(f'WEBAPP_URL={webapp_url}')
        
        with open('../.env', 'w') as f:
            f.write('\n'.join(updated_lines))
        
        print("✅ .env fayli yangilandi!")
        
    except Exception as e:
        print(f"❌ .env faylini yangilashda xatolik: {e}")

def deploy_bot():
    """Botni Railway'ga deploy qilish"""
    print("🚂 Botni Railway'ga deploy qilish...")
    
    try:
        # Railway CLI mavjudligini tekshirish
        subprocess.run(["railway", "--version"], check=True, capture_output=True)
        
        # Deploy qilish
        subprocess.run(["railway", "up"], check=True)
        print("✅ Bot muvaffaqiyatli deploy qilindi!")
        
    except subprocess.CalledProcessError:
        print("❌ Railway CLI topilmadi!")
        print("📝 O'rnatish: npm i -g @railway/cli")
    except Exception as e:
        print(f"❌ Xatolik: {e}")

if __name__ == "__main__":
    print("🚀 Deploy jarayoni boshlandi...")
    
    choice = input("1 - WebApp deploy\n2 - Bot deploy\n3 - Hammasi\nTanlang (1-3): ")
    
    if choice in ['1', '3']:
        deploy_webapp()
    
    if choice in ['2', '3']:
        deploy_bot()
    
    print("🎉 Deploy jarayoni tugadi!")
