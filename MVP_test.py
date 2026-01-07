import os
import re
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ---- Load API keys from environment variables ----
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# ---- System prompt for OpenAI ----
SYSTEM_PROMPT = """
You are a friendly German language tutor.
Your task is to help learners speak natural German.

Output format:
✅ Correct:
🌿 More natural:
📘 Explanation:
"""

# ---- Telegram message handler ----
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()

    # --- Input guard 1: too short ---
    if len(user_text.split()) < 2:
        await update.message.reply_text("Bitte sende einen vollständigen deutschen Satz 😊")
        return

    # --- Input guard 2: basic German check ---
    if not re.search(r"[äöüß]|(?:der|die|das|und|ist|ich|du|nicht|ein|eine|es|Sie|mir|dir|uns)", user_text.lower()):
        await update.message.reply_text("Bitte sende einen Satz auf Deutsch!")
        return

    # --- OpenAI API call using new SDK syntax ---
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.4
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Ups, etwas ist schief gelaufen 😢")
        print("OpenAI API error:", e)

# ---- Build and run Telegram bot ----
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot started...")
    app.run_polling()
