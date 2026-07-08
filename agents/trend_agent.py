# agents/trend_agent.py
import logging
from agents.base_agent import BaseAgent
from models.schemas import ExtractionResult, TrendReport

logger = logging.getLogger(__name__)

class TrendAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name="tencent/hy3:free")
        
        self.system_prompt = """
        Bạn là một Giám đốc Chiến lược (Chief Strategy Officer).
        Nhiệm vụ của bạn là nhận vào một danh sách các Tín hiệu Thị trường (Market Signals) rời rạc,
        sau đó tìm ra các điểm chung, kết nối chúng lại để phát hiện ra các Xu hướng lớn (Trends).
        Hãy đánh giá mức độ ảnh hưởng (impact_level) và khung thời gian (timeframe) dựa trên các tín hiệu đó.
        Đừnga quên tổng hợp danh sách các URL nguồn minh chứng cho xu hướng.
        """

    def run(self, extraction_data: ExtractionResult) -> TrendReport:
        logger.info("[Trend Agent] Bắt đầu tổng hợp các tín hiệu thành xu hướng lớn...")

        # Chuyển dữ liệu Pydantic (extraction_data) thành chuỗi JSON để truyền vào Prompt.
        json_data_string = extraction_data.model_dump_json()
        
        # Viết user_prompt truyền json_data_string vào.
        user_prompt = f"Từ các tín hiệu thị trường sau hãy phân tích xu hướng thị trường quan trọng:\n{json_data_string}"
        
        # Gọi LLM với response_format=TrendReport
        result = self.get_structured_response(system_prompt = self.system_prompt, user_prompt = user_prompt, response_format = TrendReport)
        return result