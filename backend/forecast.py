# backend/forecast.py
import requests
import pandas as pd
from datetime import datetime, timedelta, date
import geopandas as gpd
import os
import sys

# Thêm đường dẫn gốc dự án vào sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import config

# THAY TOKEN CỦA BẠN VÀO ĐÂY
WAQI_TOKEN = "64e4752250846f70bbe89e0660f45c09d90b3cb7"

# Mapping tên tỉnh WAQI → tên tiếng Việt chuẩn (63 tỉnh)
CITY_MAPPING = {
    'hanoi': 'Hà Nội',
    '@11593': 'Hồ Chí Minh',
    'thai-nguyen': 'Thái Nguyên',
    'bac-ninh': 'Bắc Ninh',
    '@14641': 'Thái Bình',
    '@13672': 'Ninh Bình',
    '@5499': 'Quảng Ninh',
    '@13028': 'Quảng Bình',
    '@13662': 'Trà Vinh',
    '@13687': 'Cần Thơ',
    '@13659': 'Tây Ninh',
    '@13417': 'Gia Lai',
    '@-476626': 'Bình Định',
    '@-476317': 'Quảng Ngãi',
    '@13658': 'Đà Nẵng',
    '@-476188': 'Hà Nam',
    'hung-yen': 'Hưng Yên',
    '@-476170': 'Hải Dương',
    'viet-tri': 'Phú Thọ',
    '@-476272': 'Long An',
}

def get_city_key(province_vn):
    """Tìm key WAQI từ tên tỉnh tiếng Việt"""
    for key, name in CITY_MAPPING.items():
        if name == province_vn:
            return key
    return None

def get_current_aqi(province_name):
    """LẤY AQI HIỆN TẠI TỪ FILE GeoJSON"""
    try:
        gdf = gpd.read_file(config.DATA_PATH)
        gdf['AQI'] = pd.to_numeric(gdf['AQI'], errors='coerce')
        row = gdf[gdf['NAME_1'] == province_name]
        if not row.empty and pd.notna(row.iloc[0]['AQI']):
            return int(row.iloc[0]['AQI'])
    except:
        pass
    return None

def get_day_name_from_offset(offset: int) -> str:
    """Trả về tên ngày theo offset (0 = hôm nay, 1 = ngày mai, ...)"""
    names = ["Hôm nay", "Ngày mai", "Ngày kia", "Ngày kia nữa", "5 ngày nữa"]
    return names[offset] if 0 <= offset < 5 else f"{offset} ngày nữa"

def is_forecast_valid(forecast_list, current_aqi):
    """
    Kiểm tra dự báo từ API có hợp lệ không:
    - Nếu tất cả các ngày đều giống nhau → LỖI
    - Nếu khác current_aqi quá nhiều → LỖI
    """
    if not forecast_list or len(forecast_list) < 2:
        return False
    
    # Kiểm tra nếu TẤT CẢ các ngày đều có cùng 1 giá trị AQI
    unique_values = set(item["aqi"] for item in forecast_list)
    if len(unique_values) == 1:
        # Tất cả đều giống nhau → có thể là lỗi API
        single_value = list(unique_values)[0]
        # Nếu giá trị này khác xa current_aqi → chắc chắn lỗi
        if current_aqi and abs(single_value - current_aqi) > 50:
            return False
    
    return True

def get_forecast_real(province_name: str):
    """Lấy dự báo AQI 5 ngày - TỰ ĐỘNG PHÁT HIỆN DỮ LIỆU LỖI"""
    city_key = get_city_key(province_name)
    current_aqi = get_current_aqi(province_name)
    
    if not city_key or current_aqi is None:
        return get_forecast_fake(province_name)
    
    url = f"https://api.waqi.info/feed/{city_key}/?token={WAQI_TOKEN}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return get_forecast_fake(province_name)
        
        data = response.json()
        if data.get("status") != "ok":
            return get_forecast_fake(province_name)
        
        raw_forecast = data["data"]["forecast"]["daily"]["pm25"]
        
        # Ép về định dạng datetime
        forecast_days = []
        for item in raw_forecast:
            try:
                day_date = datetime.strptime(item["day"], "%Y-%m-%d").date()
                forecast_days.append({
                    "date": day_date,
                    "aqi": int(item["avg"])
                })
            except:
                continue
        
        today = date.today()
        result = []
        
        # Tạo dự báo 5 ngày
        for i in range(5):
            target_date = today + timedelta(days=i)
            
            if i == 0:
                # Ngày hôm nay = AQI hiện tại
                aqi = current_aqi
            else:
                # Tìm trong dữ liệu API
                match = None
                for item in forecast_days:
                    if item["date"] == target_date:
                        match = item
                        break
                
                if match:
                    aqi = match["aqi"]
                else:
                    # Không có trong API → dùng giá trị gần nhất
                    closest = min(forecast_days, key=lambda x: abs((x["date"] - target_date).days), default=None)
                    aqi = closest["aqi"] if closest else current_aqi + (i * 5)
            
            result.append({
                "date": target_date.strftime("%d/%m"),
                "day": get_day_name_from_offset(i),
                "aqi": int(aqi),
                "status": get_status(aqi),
                "color": get_color(aqi)
            })
        
        # ✅ KIỂM TRA DỮ LIỆU API CÓ HỢP LỆ KHÔNG
        if not is_forecast_valid(result[1:], current_aqi):  # Bỏ qua ngày hôm nay
            print(f"⚠️ API WAQI trả về dữ liệu lỗi cho {province_name} → dùng dự báo mô phỏng")
            return get_forecast_fake(province_name)
        
        return result
        
    except Exception as e:
        print(f"Lỗi API WAQI ({province_name}): {e}")
        return get_forecast_fake(province_name)

def get_status(aqi):
    aqi = int(aqi)
    if aqi <= 50: return "Tốt"
    elif aqi <= 100: return "Trung bình"
    elif aqi <= 150: return "Kém"
    elif aqi <= 200: return "Xấu"
    elif aqi <= 300: return "Rất xấu"
    else: return "Nguy hại"

def get_color(aqi):
    aqi = int(aqi)
    if aqi <= 50: return "#00e400"
    elif aqi <= 100: return "#cccc16"
    elif aqi <= 150: return "#ff7e00"
    elif aqi <= 200: return "#ff0000"
    elif aqi <= 300: return "#99004c"
    else: return "#4d0000"

def get_forecast_fake(province_name):
    """Dự báo mô phỏng khi API lỗi - DỰA TRÊN AQI HIỆN TẠI"""
    current_aqi = get_current_aqi(province_name)
    if current_aqi is None:
        current_aqi = 60  # Giá trị mặc định
    
    import numpy as np
    np.random.seed(hash(province_name) % 2**32)
    
    today = date.today()
    data = []
    
    for i in range(5):
        if i == 0:
            aqi = current_aqi  # Hôm nay = AQI hiện tại
        else:
            # Dao động ±20% so với current_aqi
            variation = np.random.randint(-int(current_aqi*0.15), int(current_aqi*0.2))
            aqi = max(10, min(300, current_aqi + variation))
        
        target_date = today + timedelta(days=i)
        
        data.append({
            "date": target_date.strftime("%d/%m"),
            "day": get_day_name_from_offset(i),
            "aqi": int(aqi),
            "status": get_status(aqi),
            "color": get_color(aqi)
        })
    
    return data

def get_forecast(province_name: str):
    """HÀM CHÍNH - Lấy dự báo 5 ngày"""
    return get_forecast_real(province_name)