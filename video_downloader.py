import os
import sys
from url_utils import validate_url
from youtube_downloader import YouTubeDownloader
from tiktok_downloader import TikTokDownloader
from config import DOWNLOAD_DIR

def main():
    # Create download directory if it doesn't exist
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    # Initialize downloaders
    youtube_downloader = YouTubeDownloader()
    tiktok_downloader = TikTokDownloader()
    
    # Print welcome message
    print("\nVideo Downloader CLI")
    print("====================")
    
    while True:
        print("\nOptions:")
        print("1. Download from YouTube")
        print("2. Download from TikTok")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            url = input("Enter YouTube URL: ")
            print("Downloading YouTube video...")
            filepath = youtube_downloader.download_video(url)
            if filepath:
                print(f"Success! Video downloaded to: {filepath}")
            else:
                print("Failed to download the video.")
        
        elif choice == '2':
            url = input("Enter TikTok URL: ")
            print("Downloading TikTok video...")
            filepath = tiktok_downloader.download_video(url)
            if filepath:
                print(f"Success! Video downloaded to: {filepath}")
            else:
                print("Failed to download the video.")
        
        elif choice == '3':
            print("Exiting...")
            sys.exit(0)
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main() 