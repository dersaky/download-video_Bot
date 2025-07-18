import os

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')

# TikTok settings
TIKTOK_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# YouTube settings
YOUTUBE_QUALITY = "best"

# Telegram settings
# Чтобы получить токен:
# 1. Откройте Telegram и найдите @BotFather
# 2. Отправьте команду /newbot и следуйте инструкциям
# 3. После создания бота вы получите токен, который нужно вставить ниже
TELEGRAM_TOKEN = "8082961558:AAHOf7GjX6uSsJCiuzeaK9F-IgCNvRXQEEw"  # Ваш токен от BotFather 