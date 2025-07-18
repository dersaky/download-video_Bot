import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Download settings
DOWNLOAD_DIR = "downloads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB max file size for Telegram

# Create download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR) 