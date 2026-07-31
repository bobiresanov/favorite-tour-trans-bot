import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

COMPANY_INFO = """
KOMPANIYA: FAVORITE TOUR TRANS
Maqsad: Khalqaro yuk tashuvchi haydovchilar uchun visa consulting

ASOSIY XIZMATLARI:

1. SHÉNGEN C VIZALARI:
   🇱🇹 LITVA - 330 USD (2-4 hafta)
   🇱🇻 LATVIYA - 370 USD (10-15 kun)
   🇩🇪 GERMANIYA - 470 USD (2-3 oy)

2. МАП (CODE 95) - 950,000 сўм (4 kun)
3. ADR (ДОПОГ) - 850,000 сўм (3 kun)
4. ADR (TSISTERNA) - 350,000 сўм (1 kun)
5. TEST-DRIVE - 400,000-350,000 сўм/soat
6. SUGORTA - Rossiya, Qozog'iston
7. TAKHOGRAF - 1,700,000 сўм (20-30 kun)

KONTAKT:
📱 Telegram: @shaxlovisa
☎️ +998 97 798 10 77
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Assalomu alaykum! 👋

🚛 FAVORITE TOUR TRANS - AI Konsultant Bot

Istalgan savol bering - AI sizga javob beradı! 🤖
    """)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    loading_msg = await update.message.reply_text("🤔 AI javob bermoqdaman...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Siz FAVORITE TOUR TRANS AI konsultantsiz. Uzbek tilida professional javob bering.\n\n{COMPANY_INFO}"
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
