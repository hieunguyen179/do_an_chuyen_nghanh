# 🌍 AirWatch VN - Hệ Thống Giám Sát Chất Lượng Không Khí (AQI) Real-time

**AirWatch VN** là một ứng dụng WebGIS hiện đại nhằm theo dõi, phân tích và dự báo chỉ số chất lượng không khí (AQI) tại Việt Nam. Dự án kết hợp sức mạnh của dữ liệu thời gian thực từ API và các kỹ thuật xử lý dữ liệu không gian để cung cấp cái nhìn trực quan nhất cho người dùng.

## ✨ Tính năng nổi bật

- **Dữ liệu thời gian thực:** Tự động thu thập chỉ số AQI từ các trạm đo thông qua World Air Quality Index (WAQI) API.
- **Xử lý nội suy không gian (IDW):** Sử dụng thuật toán Inverse Distance Weighting để tính toán chỉ số AQI cho các vùng không có trạm đo, giúp phủ kín bản đồ dữ liệu.
- **Bản đồ tương tác:** Hiển thị dữ liệu trực quan trên nền bản đồ GIS, hỗ trợ xem chi tiết theo từng tỉnh/thành phố.
- **Dự báo & Lịch sử:** Cung cấp biểu đồ theo dõi lịch sử thay đổi chỉ số AQI và đưa ra các dự báo dựa trên dữ liệu thu thập được.
- **Cập nhật tự động:** Tích hợp bộ lập lịch (Scheduler) giúp hệ thống luôn tự làm mới dữ liệu vào 8:00 AM mỗi ngày.

## 🛠 Công nghệ sử dụng

- **Backend:** Python 3.10+
- **Frontend:** Streamlit (với Folium và Plotly)
- **Cơ sở dữ liệu:** SQLite (Lưu trữ lịch sử AQI)
- **Xử lý dữ liệu:** Pandas, Geopandas, Scipy
- **GIS:** Shapefiles Việt Nam (GADM), GeoJSON

## 🚀 Hướng dẫn cài đặt nhanh

### 1. Yêu cầu hệ thống

- Python 3.10 trở lên.
- Tài khoản lấy API Token tại [aqicn.org](https://aqicn.org/data-platform/token/).

### 2. Thiết lập môi trường

1. Tạo môi trường ảo: `python -m venv env`
2. Kích hoạt môi trường ảo: `.\env\Scripts\activate` (Windows)
3. Cài đặt thư viện: `pip install -r requirements.txt`

### 3. Cấu hình

Tạo file `.env` tại thư mục gốc và thêm mã API của bạn:

```env
API_KEY=your_api_token_here
```
