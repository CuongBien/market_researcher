import os
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_web(query: str, max_results: int = 3) -> list[str]:
    logger.info(f"Đang tìm kiếm bằng Serper (Google Search) với từ khóa: {query}")
    api_key = os.getenv("SERPER_API_KEY")
    
    if not api_key:
        logger.error("LỖI: Chưa có SERPER_API_KEY trong file .env")
        return []
        
    try:
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": query,
            "num": max_results
        })
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        urls = [r['link'] for r in data.get('organic', [])]
        
        if not urls:
            logger.warning("Serper không tìm thấy kết quả.")
            
        return urls
    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm với Serper: {e}")
        return []