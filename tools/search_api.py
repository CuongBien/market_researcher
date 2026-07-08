# tools/search_api.py
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_web(query: str, max_results: int = 3) -> list[str]:
    logger.info(f"Đang tìm kiếm trên web với từ khóa: {query}")
    try:
        return [f"https://example.com/article{i}" for i in range(1, max_results + 1)]
    except Exception as e:
        logger.error(f"Lỗi khi tìm kiếm web: {e}")
        return []