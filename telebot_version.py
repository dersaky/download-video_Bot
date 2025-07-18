import os
import logging
import telebot
from config import DOWNLOAD_DIR, TELEGRAM_TOKEN
from youtube_downloader import YouTubeDownloader
from tiktok_downloader import TikTokDownloader

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Initialize downloaders
youtube_downloader = YouTubeDownloader()
tiktok_downloader = TikTokDownloader()

# Create download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send welcome message when /start command is received"""
    bot.reply_to(message, 
                f"Привет, {message.from_user.first_name}! Я бот для скачивания видео с YouTube и TikTok.\n"
                "Просто отправь мне ссылку на видео, и я скачаю его для тебя.")

@bot.message_handler(commands=['help'])
def send_help(message):
    """Send help message when /help command is received"""
    bot.reply_to(message, 
                "Отправь мне ссылку на видео с YouTube или TikTok, и я скачаю его для тебя.\n"
                "Доступные команды:\n"
                "/start - Начать работу с ботом\n"
                "/help - Показать справку")

@bot.message_handler(func=lambda message: True)
def process_url(message):
    """Process URL sent by user"""
    url = message.text
    
    # Check if URL is from YouTube
    if 'youtube.com' in url or 'youtu.be' in url:
        download_youtube_video(message, url)
    # Check if URL is from TikTok
    elif 'tiktok.com' in url:
        download_tiktok_video(message, url)
    else:
        bot.reply_to(message, 
                    "Извините, я могу скачивать видео только с YouTube и TikTok.\n"
                    "Пожалуйста, отправьте корректную ссылку.")

def download_youtube_video(message, url):
    """Download a video from YouTube and send it to the user"""
    bot.reply_to(message, "Скачиваю видео с YouTube...")
    
    try:
        filepath = youtube_downloader.download_video(url)
        
        if filepath and os.path.exists(filepath):
            # Send the video to the user
            with open(filepath, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file, caption="Вот ваше видео с YouTube!")
            # Remove the file after sending
            os.remove(filepath)
        else:
            bot.reply_to(message, "Не удалось скачать видео. Пожалуйста, проверьте ссылку и попробуйте снова.")
    
    except Exception as e:
        logger.error(f"Error downloading YouTube video: {str(e)}")
        bot.reply_to(message, "Произошла ошибка при скачивании видео. Пожалуйста, попробуйте позже.")

def download_tiktok_video(message, url):
    """Download a video from TikTok and send it to the user"""
    bot.reply_to(message, "Скачиваю видео с TikTok...")
    
    try:
        filepath = tiktok_downloader.download_video(url)
        
        if filepath and os.path.exists(filepath):
            # Send the video to the user
            with open(filepath, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file, caption="Вот ваше видео с TikTok!")
            # Remove the file after sending
            os.remove(filepath)
        else:
            bot.reply_to(message, "Не удалось скачать видео. Пожалуйста, проверьте ссылку и попробуйте снова.")
    
    except Exception as e:
        logger.error(f"Error downloading TikTok video: {str(e)}")
        bot.reply_to(message, "Произошла ошибка при скачивании видео. Пожалуйста, попробуйте позже.")

if __name__ == "__main__":
    # Check if token is set
    if TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Пожалуйста, установите ваш токен бота в файле config.py")
        print("ОШИБКА: Токен бота не установлен!")
        print("Пожалуйста, откройте файл config.py и замените 'YOUR_BOT_TOKEN_HERE' на ваш токен от @BotFather")
        exit(1)
        
    print("Запускаю Telegram бота...")
    print("Бот запущен! Откройте Telegram и найдите своего бота, чтобы начать.")
    print("Нажмите Ctrl+C для остановки бота.")
    
    # Start the bot
    bot.polling(none_stop=True) 