# AirWatch GIS real-time

Tài liệu hướng dẫn cài đặt và chạy dự án trên Windows.

### Yêu cầu hệ thống
- Python 3.10+ đã cài đặt (`py -3 --version` để kiểm tra)
- Git (tùy chọn nếu bạn cần clone dự án)
- PowerShell hoặc Command Prompt

### 1) Tạo môi trường ảo và cài đặt phụ thuộc
Trong thư mục gốc dự án (`C:\Do_An_Chuyen_Nganh\AQI`):

```bash
py -3 -m venv env
./env/Scripts/Activate.ps1
pip install -r requirements.txt
```

Nếu PowerShell chặn script khi kích hoạt, chạy tạm thời:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
./env/Scripts/Activate.ps1
```

### 2) Cấu hình
- Mở file `config.py` ở thư mục gốc và thêm các thông số/API key cần thiết (ví dụ: khóa truy cập dịch vụ AQI, thông tin kết nối, v.v.).

### 3) Chuẩn bị dữ liệu
- Tải/bổ sung bộ shapefile vào `data/raw` (các tệp thường gồm: `.shp`, `.dbf`, `.shx`, khuyến nghị kèm `.prj`, `.cpg`).
- Tạo thư mục đầu ra nếu chưa có:

```bash
mkdir data/processed
```

### 4) Chạy thu thập và xử lý dữ liệu
- Thu thập AQI thời gian thực:

```bash
py backend/fetch_aqi.py
```

- Xử lý dữ liệu (nếu dự án có script tương ứng):

```bash
py backend/data_processing.py
py -m backend.data_processing
```

### 5) Khởi chạy ứng dụng
- Chạy ứng dụng chính (nếu áp dụng):

```bash
py run.py
```

- Tùy chọn: bật lịch (scheduler) trên Windows:

```bash
start start_scheduler.bat
```

### Thư mục và log
- Nhật ký hệ thống (nếu có) được lưu trong thư mục `logs`.

### Gỡ lỗi nhanh
- Lỗi kích hoạt môi trường ảo trên PowerShell: dùng lệnh `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` rồi kích hoạt lại.
- Nếu thiếu thư viện: đảm bảo đã kích hoạt môi trường ảo và chạy `pip install -r requirements.txt`.

---
Mọi thắc mắc hoặc góp ý, vui lòng cập nhật trong `docs/` hoặc tạo issue trên repository.
