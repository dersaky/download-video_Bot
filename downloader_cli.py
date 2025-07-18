import os
import logging
import sys

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Simple script to test the downloaders without Telegram bot functionality"""
    from config import DOWNLOAD_DIR
    from youtube_downloader import YouTubeDownloader
    from tiktok_downloader import TikTokDownloader
    
    # Initialize downloaders
    youtube_downloader = YouTubeDownloader()
    tiktok_downloader = TikTokDownloader()
    
    # Create download directory if it doesn't exist
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    print("Video Downloader CLI")
    print("====================")
    print("1. Download from YouTube")
    print("2. Download from TikTok")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == '1':
        url = input("Enter YouTube URL: ")
        print("Downloading YouTube video...")
        filepath = youtube_downloader.download_video(url)
        if filepath:
            print(f"Video downloaded successfully to: {filepath}")
        else:
            print("Failed to download video.")
    
    elif choice == '2':
        url = input("Enter TikTok URL: ")
        print("Downloading TikTok video...")
        filepath = tiktok_downloader.download_video(url)
        if filepath:
            print(f"Video downloaded successfully to: {filepath}")
        else:
            print("Failed to download video.")
    
    elif choice == '3':
        sys.exit(0)
    
    else:
        print("Invalid choice.")

if __name__ == '__main__':
    main() 