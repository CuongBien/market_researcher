import logging
from duckduckgo_search import DDGS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_web(query: str, max_results: int = 3) -> list[str]:
    logger.info(f"Đang tìm kiếm trên web với từ khóa: {query}")
    try:
        results = DDGS().text(query, max_results=max_results)
        urls = [r.get('href') for r in results if r.get('href')]
        
        if not urls:
            logger.warning("DuckDuckGo trả về rỗng (có thể do Rate Limit). Đang sử dụng URL dự phòng...")
            return ["https://en.wikipedia.org/wiki/Artificial_intelligence_in_healthcare"]
            
        return urls
    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm web: {e}")
        return ["https://en.wikipedia.org/wiki/Artificial_intelligence_in_healthcare"]