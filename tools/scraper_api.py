import logging
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_website(url: str) -> str:
    """
    Hàm cào dữ liệu từ một URL.
    Trả về nội dung bài viết dưới dạng chuỗi (Text/Markdown).
    """
    logger.info(f"Đang cào dữ liệu từ URL: {url}")
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Loại bỏ các thẻ không cần thiết như script, style, nav, footer, header
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        # Ưu tiên lấy phần thẻ bài viết
        main_content = soup.find('article') or soup.find('main') or soup.body
        if not main_content:
            main_content = soup
            
        # Chuyển đổi HTML sang Markdown
        markdown_text = md(str(main_content), heading_style="ATX").strip()
        
        # Cắt bớt nếu quá dài (tránh vượt quá token limit của LLM)
        if len(markdown_text) > 15000:
            markdown_text = markdown_text[:15000] + "\n\n[Nội dung đã bị cắt bớt do quá dài]"
            
        return markdown_text

    except Exception as e:
        logger.error(f"Lỗi khi cào dữ liệu từ {url}: {e}")
        return ""