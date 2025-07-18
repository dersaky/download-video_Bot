import os
import logging
import sys
from config import DOWNLOAD_DIR, TELEGRAM_TOKEN
from youtube_downloader import YouTubeDownloader
from tiktok_downloader import TikTokDownloader

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Run the bot in simple CLI mode without Telegram integration"""
    # Initialize downloaders
    youtube_downloader = YouTubeDownloader()
    tiktok_downloader = TikTokDownloader()
    
    # Create download directory if it doesn't exist
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    print("Video Downloader Bot")
    print("===================")
    print("Проблема: Не удалось запустить Telegram бота из-за отсутствия модуля 'imghdr'.")
    print("Решение: Используйте CLI версию бота или установите Python 3.10/3.11 вместо 3.13.")
    print()
    print("1. Скачать видео с YouTube")
    print("2. Скачать видео с TikTok")
    print("3. Выход")
    
    while True:
        choice = input("Введите ваш выбор (1-3): ")
        
        if choice == '1':
            url = input("Введите URL YouTube: ")
            print("Скачиваю видео с YouTube...")
            filepath = youtube_downloader.download_video(url)
            if filepath:
                print(f"Видео успешно скачано в: {filepath}")
            else:
                print("Не удалось скачать видео.")
        
        elif choice == '2':
            url = input("Введите URL TikTok: ")
            print("Скачиваю видео с TikTok...")
            filepath = tiktok_downloader.download_video(url)
            if filepath:
                print(f"Видео успешно скачано в: {filepath}")
            else:
                print("Не удалось скачать видео.")
        
        elif choice == '3':
            print("Выход из программы...")
            sys.exit(0)
        
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
        
        print()

if __name__ == '__main__':
    try:
        # Try to import telegram modules
        from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
        from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
        
        # If successful, define Telegram bot functions
        def start(update, context):
            """Send a message when the command /start is issued."""
            user = update.effective_user
            update.message.reply_text(
                f'Привет, {user.first_name}! Я бот для скачивания видео с YouTube и TikTok.\n'
                'Просто отправь мне ссылку на видео, и я скачаю его для тебя.'
            )

        def help_command(update, context):
            """Send a message when the command /help is issued."""
            update.message.reply_text(
                'Отправь мне ссылку на видео с YouTube или TikTok, и я скачаю его для тебя.\n'
                'Доступные команды:\n'
                '/start - Начать работу с ботом\n'
                '/help - Показать справку'
            )

        def process_url(update, context):
            """Process the URL sent by the user."""
            url = update.message.text
            
            # Check if URL is from YouTube
            if 'youtube.com' in url or 'youtu.be' in url:
                download_youtube_video(update, context, url)
            # Check if URL is from TikTok
            elif 'tiktok.com' in url:
                download_tiktok_video(update, context, url)
            else:
                update.message.reply_text(
                    'Извините, я могу скачивать видео только с YouTube и TikTok.\n'
                    'Пожалуйста, отправьте корректную ссылку.'
                )

        def download_youtube_video(update, context, url):
            """Download a video from YouTube and send it to the user."""
            update.message.reply_text('Скачиваю видео с YouTube...')
            
            try:
                # Initialize downloader
                youtube_downloader = YouTubeDownloader()
                filepath = youtube_downloader.download_video(url)
                
                if filepath and os.path.exists(filepath):
                    # Send the video to the user
                    with open(filepath, 'rb') as video_file:
                        update.message.reply_video(
                            video=video_file,
                            caption=f'Вот ваше видео с YouTube!'
                        )
                    # Remove the file after sending
                    os.remove(filepath)
                else:
                    update.message.reply_text('Не удалось скачать видео. Пожалуйста, проверьте ссылку и попробуйте снова.')
            
            except Exception as e:
                logger.error(f"Error downloading YouTube video: {str(e)}")
                update.message.reply_text('Произошла ошибка при скачивании видео. Пожалуйста, попробуйте позже.')

        def download_tiktok_video(update, context, url):
            """Download a video from TikTok and send it to the user."""
            update.message.reply_text('Скачиваю видео с TikTok...')
            
            try:
                # Initialize downloader
                tiktok_downloader = TikTokDownloader()
                filepath = tiktok_downloader.download_video(url)
                
                if filepath and os.path.exists(filepath):
                    # Send the video to the user
                    with open(filepath, 'rb') as video_file:
                        update.message.reply_video(
                            video=video_file,
                            caption=f'Вот ваше видео с TikTok!'
                        )
                    # Remove the file after sending
                    os.remove(filepath)
                else:
                    update.message.reply_text('Не удалось скачать видео. Пожалуйста, проверьте ссылку и попробуйте снова.')
            
            except Exception as e:
                logger.error(f"Error downloading TikTok video: {str(e)}")
                update.message.reply_text('Произошла ошибка при скачивании видео. Пожалуйста, попробуйте позже.')

        def run_telegram_bot():
            """Start the bot."""
            # Check if token is set
            if TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE":
                logger.error("Пожалуйста, установите ваш токен бота в файле config.py")
                print("ОШИБКА: Токен бота не установлен!")
                print("Пожалуйста, откройте файл config.py и замените 'YOUR_BOT_TOKEN_HERE' на ваш токен от @BotFather")
                sys.exit(1)
                
            # Create the Updater and pass it your bot's token
            updater = Updater(TELEGRAM_TOKEN)

            # Get the dispatcher to register handlers
            dispatcher = updater.dispatcher

            # Register command handlers
            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(CommandHandler("help", help_command))

            # Register URL handler
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_url))

            # Create download directory if it doesn't exist
            if not os.path.exists(DOWNLOAD_DIR):
                os.makedirs(DOWNLOAD_DIR)

            # Start the Bot
            updater.start_polling()
            logger.info("Бот запущен и ожидает сообщений...")
            print("Бот запущен! Откройте Telegram и найдите своего бота, чтобы начать.")
            print("Нажмите Ctrl+C для остановки бота.")

            # Run the bot until you press Ctrl-C
            updater.idle()
        
        # Run the Telegram bot
        run_telegram_bot()
        
    except ModuleNotFoundError:
        # If telegram module is not available or has issues, run in CLI mode
        print("Не удалось запустить Telegram бота. Запускаю в режиме командной строки.")
        main() 