#agents/research_agent.py
import logging
from agents.base_agent import BaseAgent
from models.schemas import ResearchResult
from tools.search_api import search_web

logger = logging.getLogger(__name__)

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name = "tencent/hy3:free")
        self.system_prompt = """
        Bạn là một Chuyên gia Nghiên cứu Thị trường cấp cao. 
        Nhiệm vụ của bạn là phân tích danh sách các URL được cung cấp, đánh giá xem URL nào 
        chứa thông tin giá trị nhất cho chủ đề nghiên cứu.
        Sau đó, chọn ra tối đa 3 URLs tốt nhất, đưa ra lý do (reasoning) và từ khóa (query) phù hợp.
        """
    
    def run(self, topic: str) -> ResearchResult:
        logger.info(f"[Research Agent] Bắt đầu nghiên cứu chủ đề: {topic}")
        # Dùng hàm search_web() để tìm kiếm các URL dựa trên topic.
        raw_urls = search_web(query = topic, max_results = 3)
        
        # Tạo user_prompt.
        user_prompt = f"Chủ đề nghiên cứu: {topic}\nDanh sách URL thô thu thập được: {raw_urls}"

        result = self.get_structured_response(system_prompt = self.system_prompt, user_prompt = user_prompt, response_format = ResearchResult)
        
        # Bước 4: Return kết quả
        return result

