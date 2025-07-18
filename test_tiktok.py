import os
from tiktok_downloader import TikTokDownloader
from config import DOWNLOAD_DIR

# Create download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Initialize the TikTok downloader
downloader = TikTokDownloader()

# Test URL - replace with a real TikTok URL when running
test_url = "https://www.tiktok.com/@username/video/1234567890123456789"

print(f"Testing TikTok downloader with URL: {test_url}")
result = downloader.download_video(test_url)

if result:
    print(f"Success! Video downloaded to: {result}")
else:
    print("Failed to download the video.") 