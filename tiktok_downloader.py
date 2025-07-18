import os
import logging
import requests
import re
import uuid
from config import DOWNLOAD_DIR, TIKTOK_USER_AGENT

logger = logging.getLogger(__name__)

class TikTokDownloader:
    def __init__(self):
        logger.info("Initializing TikTok downloader")
        self.headers = {
            "User-Agent": TIKTOK_USER_AGENT,
            "Referer": "https://www.tiktok.com/"
        }
    
    def download_video(self, url):
        """Download a video from TikTok
        
        Args:
            url (str): TikTok video URL
            
        Returns:
            str: Path to downloaded file or None if download failed
        """
        try:
            logger.info(f"Downloading video from {url}")
            
            # Get the HTML content
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            html_content = response.text
            
            # Extract video URL using regex
            video_url_pattern = r'<video[^>]*src="([^"]*)"'
            video_urls = re.findall(video_url_pattern, html_content)
            
            if not video_urls:
                logger.error("Could not find video URL in TikTok page")
                return None
            
            video_url = video_urls[0]
            
            # Download the video
            video_response = requests.get(video_url, headers=self.headers)
            video_response.raise_for_status()
            
            # Generate a unique filename
            filename = f"tiktok_{uuid.uuid4().hex}.mp4"
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            
            # Save the video
            with open(filepath, 'wb') as f:
                f.write(video_response.content)
            
            logger.info(f"Video downloaded to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error downloading TikTok video: {str(e)}")
            return None 