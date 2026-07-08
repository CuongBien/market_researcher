#agents/extraction_agent.py
import logging
from agents.base_agent import BaseAgent
from models.schemas import ExtractionResult
from tools.scraper_api import scrape_website
from typing import List 

logger = logging.getLogger(__name__)

class ExtractionAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name = "poolside/laguna-xs-2.1:free")
        self.system_prompt = """
        Bạn là một Chuyên gia Phân tích Dữ liệu (Data Analyst).
        Nhiệm vụ của bạn là đọc các nội dung bài viết được cung cấp và rút trích ra các Tín hiệu thị trường (Market Signals).
        Hãy phân tích kỹ nội dung, tự suy luận để đánh giá cảm xúc (sentiment), điểm tin cậy, và phân loại tín hiệu.
        Chỉ rút trích những thông tin thực sự có giá trị kinh doanh.
        """
    
    def run(self, urls: List[str]) -> ExtractionResult:
        logger.info(f"[Extraction Agent] Bắt đầu cào và rút trích dữ liệu từ {len(urls)} URLs")
        # Khởi tạo một chuỗi rỗng để chứa toàn bộ nội dung cào đượ
        all_scraped_content = ""
        
        # Dùng vòng lặp for duyệt qua từng url trong biến `urls`.
        for url in urls:
            content = scrape_website(url)
            if content:
                all_scraped_content = all_scraped_content + "\n--- BÀI VIẾT MỚI ---\n"
                all_scraped_content = all_scraped_content + content
        
        # Tạo user_prompt chứa toàn bộ nội dung `all_scraped_content`.
        user_prompt = f"Từ dữ liệu thô thu được sau đây, hãy trích xuất ra các tín hiệu thị trường quan trọng:\n{all_scraped_content}"
        
        # Gọi LLM (self.get_structured_response) với response_format=ExtractionResult
        result = self.get_structured_response(
            system_prompt = self.system_prompt, 
            user_prompt = user_prompt, 
            response_format = ExtractionResult)
        return result