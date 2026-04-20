# run.py
import os
import sys
import threading
import time
import subprocess

# Đặt thư mục gốc dự án
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

# =================================================================
# 1. KHỞI ĐỘNG SCHEDULER (CẬP NHẬT AQI HÀNG NGÀY)
# =================================================================
def start_scheduler():
    print("Khởi động scheduler cập nhật AQI lúc 8:00 AM...")
    subprocess.Popen([sys.executable, os.path.join(PROJECT_ROOT, "backend", "scheduler.py")])
    print("Scheduler đã chạy nền!")

# =================================================================
# 2. CHẠY STREAMLIT APP
# =================================================================
def run_streamlit():
    app_path = os.path.join(PROJECT_ROOT, "frontend", "app.py")
    print(f"Khởi động Streamlit tại: http://localhost:8501")
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path, "--server.port=8501"])

# =================================================================
# 3. CHẠY CẢ HAI TRONG MỘT FILE
# =================================================================
if __name__ == "__main__":
    print("="*60)
    print("       AIRWATCH VN - HỆ THỐNG GIÁM SÁT AQI")
    print("="*60)

    # Bước 1: Khởi động scheduler (chạy nền)
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    time.sleep(2)  # Đợi scheduler khởi động

    # Bước 2: Chạy Streamlit (chặn luồng chính)
    run_streamlit()