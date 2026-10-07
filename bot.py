import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai
from google.genai import types

# Mengambil token rahasia secara aman dari pengaturan Render
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Inisialisasi klien Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
# TULIS SYSTEM INSTRUCTION KARAKTERMU DI SINI
# ==========================================
SYSTEM_INSTRUCTION = """
Kamu adalah karakter roleplay. Selalu jawab menggunakan sudut pandang orang pertama 
dan gunakan tanda bintang (*) untuk mendeskripsikan tindakan fisik atau ekspresi.
"""

# Menyimpan memori chat sementara untuk setiap user
user_chats = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    # Buat sesi chat baru jika user baru pertama kali ngobrol
    if user_id not in user_chats:
        user_chats[user_id] = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.8,
            )
        )

    chat_session = user_chats[user_id]

    try:
        # Kirim pesan ke Gemini dan tunggu balasannya
        response = chat_session.send_message(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"[Terjadi kendala sistem: {e}]")

if __name__ == '__main__':
    # Jalankan bot Telegram
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot Telegram Roleplay aktif...")
    app.run_polling()
  
