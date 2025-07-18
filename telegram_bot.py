import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from config import DOWNLOAD_DIR, TELEGRAM_TOKEN
from youtube_downloader import YouTubeDownloader
from tiktok_downloader import TikTokDownloader

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize downloaders
youtube_downloader = YouTubeDownloader()
tiktok_downloader = TikTokDownloader()

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        f'Привет, {user.first_name}! Я бот для скачивания видео с YouTube и TikTok.\n'
        'Просто отправь мне ссылку на видео, и я скачаю его для тебя.'
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Отправь мне ссылку на видео с YouTube или TikTok, и я скачаю его для тебя.\n'
        'Доступные команды:\n'
        '/start - Начать работу с ботом\n'
        '/help - Показать справку'
    )

def process_url(update: Update, context: CallbackContext) -> None:
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

def download_youtube_video(update: Update, context: CallbackContext, url: str) -> None:
    """Download a video from YouTube and send it to the user."""
    update.message.reply_text('Скачиваю видео с YouTube...')
    
    try:
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

def download_tiktok_video(update: Update, context: CallbackContext, url: str) -> None:
    """Download a video from TikTok and send it to the user."""
    update.message.reply_text('Скачиваю видео с TikTok...')
    
    try:
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

def main() -> None:
    """Start the bot."""
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
    logger.info("Bot started polling")

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main() 