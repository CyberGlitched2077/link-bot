import sqlite3
import telebot
import os

BOT_TOKEN = "8981410413:AAHzHrEf0CFHYNcw1RGhcVa6A4D37u9H1kU"
bot = telebot.TeleBot(BOT_TOKEN)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(file)), "devices.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            phone_number TEXT,
            device_type TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_user_device(chat_id, phone, device):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (chat_id, phone_number, device_type)
        VALUES (?, ?, ?)
    ''', (chat_id, phone, device))
    conn.commit()
    conn.close()

init_db()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    text_parts = message.text.split()
    
    if len(text_parts) > 1:
        payload = text_parts[1]
        
        if "_" in payload:
            try:
                user_phone, device_type = payload.split("_", 1)
                save_user_device(chat_id, user_phone, device_type)
                
                reply_text = (
                    f"✅ Device Added Successfully!\n\n"
                    f"📱 Device: {device_type}\n"
                    f"📞 Phone: {user_phone}\n"
                    f"🆔 Chat ID: {chat_id}\n\n"
                    f"የእርስዎ ዲቫይስ እና ስልክ ቁጥር በዳታቤዝ ውስጥ በተሳካ ሁኔታ ተመዝግቧል።"
                )
                bot.reply_to(message, reply_text, parse_mode="Markdown")
                
            except Exception as e:
                bot.reply_to(message, "❌ መረጃውን ለመመዝገብ ስህተት አጋጥሟል።")
        else:
            bot.reply_to(message, "❌ የሊንኩ መረጃ ቅርጸት ትክክል አይደለም።")
    else:
        bot.reply_to(message, "👋 እንኳን ደህና መጡ! ዲቫይስዎን ለመመዝገብ እባክዎ በዌብሳይቱ ሊንክ በኩል ይግቡ።")

print("ቦቱ መስራት ጀምሯል...")
bot.infinity_polling()
