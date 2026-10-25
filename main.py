import telebot
import gspread
from google.oauth2.service_account import Credentials

# 1. إعدادات التيليجرام
TELEGRAM_TOKEN = "8629600671:AAGr-wizwxAs7rCnSlQO3wPCC0kpDK3YwHI"
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 2. إعدادات الربط مع Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# فتح جدول البيانات الخاص بك
SPREADSHEET_NAME = "قائمة أسعار ومخزون أعلاف وحاصلات أبو عبيدة"
sheet = client.open(SPREADSHEET_NAME).sheet1

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك في بوت كاشير أبو عبيدة 🌾\n\n"
        "أرسل اسم أي صنف للبحث عن السعر والمخزون مباشرة."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda msg: not msg.text.startswith('/'))
def check_price(message):
    query = message.text.strip().lower()
    records = sheet.get_all_records()
    
    found = False
    for row in records:
        item_name = str(row.get('اسم الصنف', '')).lower()
        if query in item_name:
            found = True
            response = (
                f"📦 *الصنف:* {row.get('اسم الصنف')}\n"
                f"🏷️ *التصنيف:* {row.get('التصنيف')}\n"
                f"💰 *سعر البيع:* {row.get('سعر البيع (ج.م)')} ج.م / {row.get('وحدة البيع')}\n"
                f"📊 *الحالة:* {row.get('حالة الرصيد')}\n"
                f"📝 *ملاحظات:* {row.get('ملاحظات', 'لا يوجد')}"
            )
            bot.reply_to(message, response, parse_mode="Markdown")
            break
            
    if not found:
        bot.reply_to(message, "❌ لم يتم العثور على الصنف في الجدول.")

bot.infinity_polling()
