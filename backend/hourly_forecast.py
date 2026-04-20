# backend/hourly_forecast.py
from datetime import datetime, timedelta
import numpy as np
import geopandas as gpd
import config
import pandas as pd

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

def get_hourly_forecast(province_name: str):
    """
    Dự báo AQI từ GIỜ HIỆN TẠI đến 11 PM (23:00)
    Mỗi điểm cách nhau 2 TIẾNG
    Ví dụ: 10:00 AM → 12:00 PM → 2:00 PM → 4:00 PM → 6:00 PM → 8:00 PM → 10:00 PM
    """
    current_aqi = get_current_aqi(province_name)
    if current_aqi is None:
        current_aqi = 80  # Giá trị mặc định
    
    np.random.seed(hash(province_name) % 2**32)
    
    now = datetime.now()
    current_hour = now.hour
    
    # Tạo danh sách các giờ cách nhau 2 tiếng từ hiện tại đến 23:00
    hours_list = []
    h = current_hour
    while h <= 23:
        hours_list.append(h)
        h += 2
    
    # Nếu giờ cuối chưa đến 23:00, thêm 23:00 (11 PM)
    if hours_list[-1] < 23:
        hours_list.append(23)
    
    data = []
    
    for i, hour in enumerate(hours_list):
        # Giờ đầu tiên = AQI hiện tại
        if i == 0:
            aqi = current_aqi
        else:
            # Dao động ±15% so với current_aqi
            variation = np.random.randint(-int(current_aqi*0.15), int(current_aqi*0.2))
            aqi = max(10, min(300, current_aqi + variation))
        
        # Format label
        if i == 0:
            display_label = "Bây giờ"
        else:
            if hour == 0:
                display_label = "12:00 AM"
            elif hour < 12:
                display_label = f"{hour}:00 AM"
            elif hour == 12:
                display_label = "12:00 PM"
            else:
                display_label = f"{hour-12}:00 PM"
        
        # Tạo datetime object
        time_obj = datetime.combine(now.date(), datetime.min.time()) + timedelta(hours=hour)
        
        aqi = int(aqi)
        data.append({
            "time": time_obj,
            "display_label": display_label,
            "aqi": aqi,
            "status": get_status(aqi),
            "color": get_color(aqi)
        })
    
    return data

def get_status(aqi):
    if aqi <= 50: return "Tốt"
    elif aqi <= 100: return "Trung bình"
    elif aqi <= 150: return "Kém"
    elif aqi <= 200: return "Xấu"
    elif aqi <= 300: return "Rất xấu"
    else: return "Nguy hại"

def get_color(aqi):
    if aqi <= 50: return "#00e400"
    elif aqi <= 100: return "#cccc16"
    elif aqi <= 150: return "#ff7e00"
    elif aqi <= 200: return "#ff0000"
    elif aqi <= 300: return "#99004c"
    else: return "#4d0000"