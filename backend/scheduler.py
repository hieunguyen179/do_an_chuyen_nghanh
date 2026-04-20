# backend/scheduler.py
import os
import sys

# THÊM ĐƯỜNG DẪN GỐC DỰ ÁN (KHẮC PHỤC ModuleNotFoundError)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)  # Thêm vào đầu list để ưu tiên

# Cấu hình logging
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from backend.data_processing import process_data
from datetime import datetime
import time

logging.basicConfig(
    filename='logs/backend_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

def update_job():
    logging.info("BẮT ĐẦU update_job() lúc 8:00 AM")
    try:
        process_data()
        logging.info(f"AQI cập nhật thành công lúc {datetime.now()}")
    except Exception as e:
        logging.error(f"LỖI: {e}", exc_info=True)

# Khởi tạo scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(update_job, 'cron', hour=8, minute=0)
scheduler.start()

logging.info("Scheduler khởi động! Sẽ cập nhật lúc 8:00 AM hàng ngày.")

# Giữ process sống MÀ KHÔNG CHẶN .bat
try:
    while True:
        time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    logging.info("Scheduler đã dừng.")