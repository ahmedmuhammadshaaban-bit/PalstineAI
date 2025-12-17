# -*- coding: utf-8 -*-

import telebot
import google.generativeai as genai
from PIL import Image
import os
import io

# ================= TOKENS =================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# ================= GEMINI CONFIG =================
genai.configure(api_key=GEMINI_API_KEY)

# ⚠️ موديل الصور (ده الرسمي حاليًا)
image_model = genai.GenerativeModel("imagen-3")

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎨 Send /img followed by your prompt\n\nExample:\n/img historical map of Palestine vintage style"
    )

# ================= IMAGE GENERATOR =================
@bot.message_handler(commands=['img'])
def generate_image(message):
    prompt = message.text.replace("/img", "").strip()

    if not prompt:
        bot.send_message(message.chat.id, "❌ Please provide a prompt after /img")
        return

    bot.send_message(message.chat.id, "⏳ Generating image, please wait...")

    try:
        result = image_model.generate_content(
            prompt,
            generation_config={
                "image_size": "1024x1024"
            }
        )

        # استخراج الصورة
        image_bytes = result.candidates[0].content.parts[0].inline_data.data
        image = Image.open(io.BytesIO(image_bytes))

        img_io = io.BytesIO()
        image.save(img_io, format="PNG")
        img_io.seek(0)

        bot.send_photo(
            message.chat.id,
            img_io,
            caption="#Hatshepsut #Palestine"
        )

        bot.send_message(
            message.chat.id,
            "مع تحيات بشمهندس بيبو\nوشريكه محمد مختار"
        )

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error:\n{str(e)}")

# ================= RUN =================
print("Bot is running...")
bot.infinity_polling()
