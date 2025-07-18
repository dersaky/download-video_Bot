import re

def is_youtube_url(url):
    """
    Check if URL is a YouTube URL
    
    Args:
        url (str): URL to check
        
    Returns:
        bool: True if URL is from YouTube, False otherwise
    """
    youtube_patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=[\w-]+',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/[\w-]+',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/[\w-]+'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url):
            return True
    
    return False

def is_tiktok_url(url):
    """
    Check if URL is a TikTok URL
    
    Args:
        url (str): URL to check
        
    Returns:
        bool: True if URL is from TikTok, False otherwise
    """
    tiktok_patterns = [
        r'(?:https?:\/\/)?(?:www\.)?tiktok\.com\/@[\w\.]+\/video\/\d+',
        r'(?:https?:\/\/)?(?:www\.)?vm\.tiktok\.com\/[\w]+',
        r'(?:https?:\/\/)?(?:www\.)?vt\.tiktok\.com\/[\w]+'
    ]
    
    for pattern in tiktok_patterns:
        if re.match(pattern, url):
            return True
    
    return False

def validate_url(url):
    """
    Validate if URL is supported (YouTube or TikTok)
    
    Args:
        url (str): URL to validate
        
    Returns:
        tuple: (is_valid, platform) where platform is 'youtube', 'tiktok', or None
    """
    if is_youtube_url(url):
        return True, 'youtube'
    elif is_tiktok_url(url):
        return True, 'tiktok'
    else:
        return False, None 