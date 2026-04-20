# backend/data_processing.py
import geopandas as gpd
import pandas as pd
import sqlite3
from backend.fetch_aqi import fetch_aqi
import config
from datetime import datetime
from backend.interpolation import calculate_missing_aqi  # ← ĐÃ IMPORT

def process_data():
    # 1. Đọc shapefile 63 tỉnh
    gdf = gpd.read_file('data/raw/gadm41_VNM_1.shp')
    
    # 2. Lấy AQI từ API (aqi_df đã chứa tên tiếng Việt)
    aqi_df = fetch_aqi()
    
    # 3. Chuẩn bị merge:
    province_aqi = dict(zip(aqi_df['Province'], aqi_df['AQI']))
    
    # 4. GÁN AQI CHO TỈNH TRONG SHAPEFILE
    gdf = gdf.copy()
    gdf['AQI'] = gdf['NAME_1'].map(province_aqi)
    gdf['AQI'] = pd.to_numeric(gdf['AQI'], errors='coerce')
    
    # 5. XỬ LÝ NGÀY
    if 'Date' in aqi_df.columns and not aqi_df.empty:
        valid_dates = aqi_df['Date'].dropna()
        update_time = pd.to_datetime(valid_dates.iloc[0]).strftime('%Y-%m-%d %H:%M')
    else:
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    gdf['Date'] = update_time
    
    # 6. BƯỚC QUAN TRỌNG: NỘI SUY AQI CHO CÁC TỈNH CÒN THIẾU
    print("Bắt đầu nội suy AQI cho các tỉnh không có trạm đo...")
    final_gdf = calculate_missing_aqi(gdf)  # ← DÙNG BIẾN gdf ĐÚNG
    
    # 7. LƯU GeoJSON (BÂY GIỜ LÀ 63/63 TỈNH!)
    final_gdf.to_file(config.DATA_PATH, driver='GeoJSON')
    
    # 8. LƯU DB (dữ liệu thô từ API)
    conn = sqlite3.connect(config.DB_PATH)
    aqi_df.to_sql('daily_aqi', conn, if_exists='append', index=False)
    conn.close()
    
    # 9. IN LOG
    real_count = final_gdf['AQI_source'].value_counts().get('Trạm đo', 0)
    interp_count = final_gdf['AQI_source'].value_counts().get('Nội suy (IDW)', 0)
    
    print(f"XỬ LÝ HOÀN TẤT!")
    print(f"   Đã xử lý và lưu đầy đủ 63 tỉnh có dữ liệu AQI.")
    print(f"   → Trạm đo chính thức: {real_count} tỉnh")
    print(f"   → Nội suy (IDW): {interp_count} tỉnh")
    print(f"   GeoJSON đã được cập nhật tại: {config.DATA_PATH}")
    print(f"   Dữ liệu thô đã được lưu vào DB: {config.DB_PATH}")

if __name__ == '__main__':
    process_data()