# tools/scraper_api.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_website(url: str) -> str:
    """
    Hàm cào dữ liệu từ một URL.
    Trả về nội dung bài viết dưới dạng chuỗi (Text/Markdown).
    """
    logger.info(f"Đang cào dữ liệu từ URL: {url}")
    
    try:
        # Tạo dữ liệu giả lập (mock data) thay vì cào thật để tránh phụ thuộc thư viện/network
        mock_content = f"""
# Báo cáo thị trường từ {url}

## Tin tức nổi bật
- **Công nghệ**: Hãng Apple vừa ra mắt hệ thống AI mới mang tên Apple Intelligence, thúc đẩy giá cổ phiếu tăng hơn 5% trong phiên giao dịch sớm.
- **Tiêu dùng**: Xu hướng sử dụng các sản phẩm thân thiện với môi trường đang tăng mạnh trong quý 3/2024. Nhu cầu tìm kiếm "sản phẩm xanh" tăng 150% so với cùng kỳ năm ngoái.
- **Thương mại điện tử**: Thị trường giao hàng siêu tốc đang chứng kiến sự cạnh tranh khốc liệt giữa các ông lớn, chi phí vận chuyển trung bình giảm 15%.

*Thời gian cập nhật: Hôm nay*
        """
        return mock_content.strip()

    except Exception as e:
        logger.error(f"Lỗi khi cào dữ liệu từ {url}: {e}")
        return ""