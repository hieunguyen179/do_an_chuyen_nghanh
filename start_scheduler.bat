@echo off
cd /d D:\DACN\AQI\AQI
call env\Scripts\activate

echo [1/3] Đang lấy dữ liệu AQI từ API...
python -m backend.fetch_aqi

echo [2/3] Đang xử lý dữ liệu và lưu GeoJSON + DB...
python -m backend.data_processing

echo [3/3] Khởi động scheduler (chạy nền, cập nhật 8h sáng)...
start /min python -m backend.scheduler

echo.
echo HOÀN TẤT! Dữ liệu đã được cập nhật.
echo Scheduler đang chạy nền (cập nhật lúc 8:00 AM).
echo.
echo Bây giờ bạn có thể mở: python -m streamlit run frontend/app.py
timeout /t 5 >nul