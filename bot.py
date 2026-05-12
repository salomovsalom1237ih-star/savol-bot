from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = "8676719325:AAHy7EvOB1MVyQhQr5pbqr-wQe_Vx6kfOMk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Musiqa nomini yuboring"
    )

async def download_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text

    msg = await update.message.reply_text("⏳ Qidirilyapti...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)

            if "entries" in info:
                info = info["entries"][0]

            title = info["title"]
            filename = f"{title}.mp3"

        await update.message.reply_audio(
            audio=open(filename, "rb"),
            title=title
        )

        os.remove(filename)

        await msg.delete()

    except Exception as e:
        await msg.edit_text("❌ Xatolik chiqdi")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_music))

print("Bot ishladi...")
app.run_polling()
