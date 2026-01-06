from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import openai

import os

openai.api_key = os.getenv("OPENAI_API_KEY")


SYSTEM_PROMPT = """
You are a friendly German language tutor.
Your task is to help learners speak natural German.

Output format:
✅ Correct:
🌿 More natural:
📘 Explanation:
"""

import re

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # ---- Input guard: check short messages ----
    if len(user_text.split()) < 2:
        await update.message.reply_text("Bitte sende einen vollständigen deutschen Satz 😊")
        return

    # ---- Input guard: check if text is German (basic check) ----
    # Looks for German letters: ä, ö, ü, ß or common German words
    if not re.search(r"[äöüß]|(?:der|die|das|und|ist|ich|du|es|Sie|sie|mir|dir|Ihr|Ihnene|uns|nicht|ein|eine)", user_text.lower()):
        await update.message.reply_text("Bitte sende einen Satz auf Deutsch!")
        return

    # ---- OpenAI API call ----
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0.4
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)


    


app = ApplicationBuilder().token("8500610410:AAE_DiW7lW71__8kSOIS_5zrUsyo8WqUk3g").build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
