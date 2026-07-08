# main.py
import logging
from agents.research_agent import ResearchAgent
from agents.extraction_agent import ExtractionAgent
from agents.trend_agent import TrendAgent
from agents.brief_agent import BriefAgent

# Thiết lập logging để xem tiến trình chạy đẹp mắt
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    topic = "Phân tích xu hướng phát triển của Trí tuệ Nhân tạo (AI) trong lĩnh vực y tế năm 2026"
    logger.info(f"BẮT ĐẦU CHẠY PIPELINE NGHIÊN CỨU: {topic}")

    # Khởi tạo các Agents
    researcher = ResearchAgent()
    extractor = ExtractionAgent()
    trender = TrendAgent()
    briefer = BriefAgent()

    try:
        research_result = researcher.run(topic)
        extraction_result = extractor.run(research_result.top_urls)
        trend_result = trender.run(extraction_result)
        final_report = briefer.run(trend_result)
        
        # Lưu kết quả ra file
        logger.info("Đang lưu báo cáo ra file final_report.md...")
        with open("final_report.md", "w", encoding="utf-8") as f:
            f.write(final_report)
            
        logger.info("PIPELINE HOÀN THÀNH XUẤT SẮC!")

    except Exception as e:
        logger.error(f"Pipeline thất bại vì lỗi: {e}")

if __name__ == "__main__":
    main()