import os
import yt_dlp
from config import DOWNLOAD_DIR

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
        }
    
    def download_video(self, url):
        """
        Download video from YouTube URL
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            str: Path to downloaded file or None if download failed
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    video_id = info.get('id', '')
                    extension = info.get('ext', 'mp4')
                    filepath = os.path.join(DOWNLOAD_DIR, f"{video_id}.{extension}")
                    
                    # Check if file exists and is not empty
                    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                        return filepath
                    else:
                        return None
                else:
                    return None
        except Exception as e:
            print(f"Error downloading YouTube video: {e}")
            return None 