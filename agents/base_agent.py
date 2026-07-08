# agents/base_agent.py
import os
import logging
from openai import OpenAI
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, model_name: str = "tencent/hy3:free"): 
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        ) 
        self.model_name = model_name
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_structured_response(self, system_prompt: str, user_prompt: str, response_format: type[BaseModel]):
        logger.info(f"Đang gọi OpenRouter API với model: {self.model_name}")
        schema_json = response_format.model_json_schema()
        system_prompt_with_json = (
            f"{system_prompt}\n\n"
            f"QUAN TRỌNG: Bạn BẮT BUỘC phải trả về kết quả dưới dạng JSON hợp lệ. "
            f"Không giải thích thêm. Cấu trúc JSON phải tuân theo Schema sau:\n{schema_json}"
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt_with_json},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1, # Giảm độ sáng tạo để JSON chuẩn xác hơn
                extra_body={
                    "reasoning": {"enabled": True}
                }
            )
            # 1. Lấy nội dung chuỗi (raw text) từ kết quả trả về
            raw_content = response.choices[0].message.content.strip()
            # 2. XÓA BỎ MARKDOWN
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            elif raw_content.startswith("```"):
                raw_content = raw_content[3:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]
            raw_content = raw_content.strip()
            # 3. CONVERT THÀNH PYDANTIC MODEL VÀ RETURN
            return response_format.model_validate_json(raw_content) 
        except Exception as e:
            logger.error(f"Lỗi khi gọi LLM hoặc Parse JSON: {e}")
            raise e

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_text_response(self, system_prompt: str, user_prompt: str) -> str:
        """Hàm dùng cho các Agent cần trả về văn bản thuần túy (Markdown/Text)"""
        logger.info(f"Đang gọi OpenRouter API (Text Mode) với model: {self.model_name}")
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7 # Tăng tính sáng tạo (nhiệt độ) lên 0.7 để văn phong mềm mại hơn
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Lỗi khi gọi LLM (Text Mode): {e}")
            raise e