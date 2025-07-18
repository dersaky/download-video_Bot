import os
import logging
from pytube import YouTube
from config import DOWNLOAD_DIR, YOUTUBE_QUALITY

logger = logging.getLogger(__name__)

class YouTubeDownloader:
    def __init__(self):
        logger.info("Initializing YouTube downloader")
        
    def download_video(self, url):
        """Download a video from YouTube
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            str: Path to downloaded file or None if download failed
        """
        try:
            logger.info(f"Downloading video from {url}")
            yt = YouTube(url)
            
            # Get the best quality stream
            if YOUTUBE_QUALITY == "best":
                stream = yt.streams.get_highest_resolution()
            else:
                stream = yt.streams.filter(progressive=True).first()
            
            # Download the video
            filename = stream.default_filename
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            stream.download(output_path=DOWNLOAD_DIR)
            
            logger.info(f"Video downloaded to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error downloading YouTube video: {str(e)}")
            return None 