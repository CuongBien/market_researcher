from pydantic import BaseModel, Field
from typing import List, Optional

# Research Agent Output
class ResearchResult(BaseModel):
    query: str = Field(..., description="Từ khóa dùng để tìm kiếm")
    reasoning: str = Field(..., description="Lý do chọn các URL này để tối ưu hóa kết quả")
    top_urls: List[str] = Field(..., description="Danh sách URL quan trọng tìm được")

# Extraction Agent Output
class MarketSignal(BaseModel):
    """Đại diện cho một tín hiệu/thông tin thị trường rút trích từ 1 bài viết"""
    source_url: str = Field(..., description="URL của bài viết")
    title: str = Field(..., description="Tiêu đề của bài viết")
    summary: str = Field(..., description="Tóm tắt nội dung chính của bài viết")
    reliability_score: int = Field(..., description="Điểm tin cậy của bài viết dựa trên nguồn (0-100)")
    published_date: Optional[str] = Field(None, description="Thời gian xuất bản bài viết (nếu có)")
    signal_category: str = Field(..., description="Phân loại tín hiệu (ví dụ: Nhu cầu người dùng, Đối thủ, Công nghệ, ...)")
    sentiment: str = Field(..., description="Nhãn cảm xúc (Tích cực / Tiêu cực / Trung lập)")
    key_takeaway: str = Field(..., description="Điểm cốt lõi rút ra được từ bài viết")

class ExtractionResult(BaseModel):
    signals: List[MarketSignal] = Field(..., description="Danh sách các tín hiệu thị trường")

# Trend Agent Output
class Trend(BaseModel):
    """Đại diện cho một xu hướng thị trường tổng hợp từ nhiều tín hiệu"""
    trend_name: str = Field(..., description="Tên của xu hướng")
    trend_description: str = Field(..., description="Mô tả chi tiết của xu hướng")
    timeframe: Optional[str] = Field(None, description="Khung thời gian ước tính của xu hướng (ví dụ: Q1 2024, Hiện tại,...)")
    impact_level: str = Field(..., description="Mức độ ảnh hưởng của xu hướng (Cao / Trung bình / Thấp)")
    trend_source_url_list: List[str] = Field(..., description="Danh sách URL của các tín hiệu chứng minh cho xu hướng này")

class TrendReport(BaseModel):
    trends: List[Trend] = Field(..., description="Danh sách các xu hướng thị trường")