import telebot
import requests

BOT_TOKEN = "8107500430:AAEsPJ2H4Vbj017JSKWOadCcPmUF6QZRb2I"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет 👋 Отправь ссылку на TikTok, я скачаю видео без водяного знака 🎥")

@bot.message_handler(func=lambda message: 'tiktok.com' in message.text)
def download_tiktok(message):
    video_url = message.text.strip()
    bot.reply_to(message, "⏳ Обрабатываю ссылку, подожди немного...")

    try:
        api_url = f"https://tikwm.com/api/?url={video_url}"
        response = requests.get(api_url)
        data = response.json()

        if data and "data" in data and "play" in data["data"]:
            download_link = data["data"]["play"]

            video = requests.get(download_link)
            with open("video.mp4", "wb") as f:
                f.write(video.content)

            bot.send_video(message.chat.id, open("video.mp4", "rb"), caption="🎬 Готово! Вот видео без водяного знака ✨")

        else:
            bot.reply_to(message, "❌ Не удалось получить видео. Попробуй другую ссылку.")

    except Exception as e:
        bot.reply_to(message, f"Ошибка при скачивании: {e}")

bot.polling(none_stop=True)



