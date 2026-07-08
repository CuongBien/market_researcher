# agents/brief_agent.py
import logging
from agents.base_agent import BaseAgent
from models.schemas import TrendReport

logger = logging.getLogger(__name__)

class BriefAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name="poolside/laguna-xs-2.1:free")
        
        self.system_prompt = """
        Bạn là một Chuyên gia Viết báo cáo (Technical Writer).
        Nhiệm vụ của bạn là nhận dữ liệu JSON về các xu hướng thị trường, 
        sau đó viết một bản báo cáo chuyên nghiệp bằng định dạng Markdown.
        Báo cáo cần có:
        - Tiêu đề hấp dẫn
        - Tóm tắt điều hành (Executive Summary)
        - Chi tiết các xu hướng (Mô tả, Mức độ ảnh hưởng, Thời gian)
        - Trích dẫn nguồn (URLs) rõ ràng ở cuối.
        Chỉ in ra nội dung báo cáo Markdown, không nói thêm lời thừa.
        """

    def run(self, trend_data: TrendReport) -> str:
        logger.info("[Brief Agent] Bắt đầu viết báo cáo Markdown...")

        # Biến trend_data thành chuỗi JSON
        json_data_string = trend_data.model_dump_json()

        # Tạo user_prompt
        user_prompt = f"Dựa vào những xu hướng thị trường sau đây hãy viết cho tôi bản brief:\n {json_data_string}"
        
        # Gọi self.get_text_response()
        result = self.get_text_response(
            system_prompt = self.system_prompt, 
            user_prompt = user_prompt)
        
        # Return kết quả chuỗi
        return result