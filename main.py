import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI

# Logging sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables check
TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

logger.info(f"TOKEN: {TOKEN[:20] if TOKEN else 'NOT SET'}...")
logger.info(f"OPENAI_KEY: {OPENAI_KEY[:20] if OPENAI_KEY else 'NOT SET'}...")

if not TOKEN or not OPENAI_KEY:
    logger.error("❌ Environment variables not set!")
    exit(1)

client = OpenAI(api_key=OPENAI_KEY)

COMPANY_INFO = """
KOMPANIYA: FAVORITE TOUR TRANS
Maqsad: Khalqaro yuk tashuvchi haydovchilar uchun visa consulting

ASOSIY XIZMATLARI:

1. SHÉNGEN C VIZALARI:
   🇱🇹 LITVA - 330 USD (2-4 hafta)
   🇱🇻 LATVIYA - 370 USD (10-15 kun)
   🇩🇪 GERMANIYA - 470 USD (2-3 oy)

2. МАП (CODE 95) - 950,000 сўм
3. ADR (ДОПОГ) - 850,000 сўм
4. ADR (TSISTERNA) - 350,000 сўм
5. TEST-DRIVE - 400,000-350,000 сўм/soat
6. SUGORTA - Rossiya, Qozog'iston
7. TAKHOGRAF - 1,700,000 сўм

KONTAKT: @shaxlovisa | +998 97 798 10 77
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! 👋\n\n🚛 FAVORITE TOUR TRANS\n\nSavol bering!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    loading_msg = await update.message.reply_text("🤔 Javob bermoqdaman...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"FAVORITE TOUR TRANS AI konsultanti. Uzbek tilida.\n\n{COMPANY_INFO}"
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        ai_response = response.choices[0].message.content
        await loading_msg.delete()
        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await loading_msg.delete()
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")

def main():
    logger.info("Bot starting...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot running...")
    application.run_polling()

if __name__ == '__main__':
    main()
