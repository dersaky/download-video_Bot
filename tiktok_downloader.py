import os
import requests
import re
import json
from config import DOWNLOAD_DIR

class TikTokDownloader:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def download_video(self, url):
        """
        Download video from TikTok URL without watermark
        
        Args:
            url (str): TikTok video URL
            
        Returns:
            str: Path to downloaded file or None if download failed
        """
        try:
            # Extract video ID from URL
            video_id = self._extract_video_id(url)
            if not video_id:
                return None
            
            # Use TikWM API to get no-watermark video
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = requests.get(api_url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    video_url = data.get("data", {}).get("play")
                    if video_url:
                        # Download the video
                        video_response = requests.get(video_url, headers=self.headers)
                        if video_response.status_code == 200:
                            filepath = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
                            with open(filepath, "wb") as f:
                                f.write(video_response.content)
                            
                            # Check if file exists and is not empty
                            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                                return filepath
            
            # If TikWM fails, try alternative method (SnapTik)
            return self._try_alternative_download(url, video_id)
        
        except Exception as e:
            print(f"Error downloading TikTok video: {e}")
            return None
    
    def _extract_video_id(self, url):
        """Extract TikTok video ID from URL"""
        patterns = [
            r'video/(\d+)',
            r'tiktok\.com/.*?/video/(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _try_alternative_download(self, url, video_id):
        """Try alternative download method if primary fails"""
        try:
            # Try SnapTik API
            api_url = "https://api.snaptik.com/video-info"
            payload = {"url": url}
            response = requests.post(api_url, headers=self.headers, data=payload)
            
            if response.status_code == 200:
                data = response.json()
                video_urls = [item.get("url") for item in data.get("video", []) 
                              if item.get("type") == "no-watermark"]
                
                if video_urls:
                    video_response = requests.get(video_urls[0], headers=self.headers)
                    if video_response.status_code == 200:
                        filepath = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
                        with open(filepath, "wb") as f:
                            f.write(video_response.content)
                        
                        # Check if file exists and is not empty
                        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                            return filepath
            
            return None
        
        except Exception as e:
            print(f"Error in alternative TikTok download: {e}")
            return None 