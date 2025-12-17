# -*- coding: utf-8 -*-

import telebot
import google.generativeai as genai
import os

# ================= ENV VARIABLES =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN or not GEMINI_API_KEY:
    raise Exception("Missing BOT_TOKEN or GEMINI_API_KEY")

# ================= TELEGRAM BOT =================
bot = telebot.TeleBot(BOT_TOKEN)

# ================= GEMINI CONFIG =================
genai.configure(api_key=GEMINI_API_KEY)

# ✅ موديل مستقر 100%
model = genai.GenerativeModel("gemini-1.5-pro")

# ================= START =================
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎨 Image Generation Bot\n\n"
        "Use:\n"
        "/img <your prompt>\n\n"
        "Example:\n"
        "/img historical map of Palestine vintage style"
    )

# ================= IMAGE COMMAND =================
@bot.message_handler(commands=["img"])
def generate_image(message):
    prompt = message.text.replace("/img", "", 1).strip()

    if not prompt:
        bot.send_message(message.chat.id, "❌ Please write a prompt after /img")
        return

    bot.send_message(message.chat.id, "⏳ Generating image concept, please wait...")

    try:
        ai_prompt = f"""
Create a highly detailed AI image concept based on the following description.
Return ONLY a direct image generation prompt or visual description suitable for AI image generation:

{prompt}
"""

        response = model.generate_content(ai_prompt)

        result_text = response.text.strip()

        bot.send_message(
            message.chat.id,
            f"🖼️ Image Prompt Generated:\n\n{result_text}\n\n#Hatshepsut #Palestine"
        )

        bot.send_message(
            message.chat.id,
            "مع تحيات بشمهندس بيبو\nوشريكه محمد مختار"
        )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            "❌ An error occurred while generating the image.\nPlease try again later."
        )

# ================= RUN =================
print("Bot is running...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
