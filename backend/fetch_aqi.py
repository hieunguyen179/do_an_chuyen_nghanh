# backend/fetch_aqi.py
import requests
import pandas as pd
from datetime import datetime
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import config 

def fetch_aqi():
    aqi_data = []
    for province in config.PROVINCES_LIST:
        url = f'https://api.waqi.info/feed/{province}/?token={config.API_KEY}'
        #url = f'https://api.waqi.info/feed/{province}/?token={api}'
        response = requests.get(url).json()
        #print("Response for", province, ":", response)  # Debug
        if response.get('status') == 'ok' and isinstance(response.get('data'), dict):
            aqi = response['data'].get('aqi')
            if aqi == '-' or aqi is None or aqi == '':
                aqi = None
                #print(f"Cảnh báo: AQI thiếu cho {province}.")
        else:
            aqi = None
        aqi_data.append({'Province': config.PROVINCE_MAPPING.get(province, province), 'AQI': aqi, 'Date': datetime.now()})
    return pd.DataFrame(aqi_data)

if __name__ == '__main__':
    df = fetch_aqi()
    valid_aqi_df = df[df['AQI'].notna()]
    valid_aqi_df.to_csv('data/raw/initial_aqi.csv', index=False)  # Lưu CSV ban đầu
    
    valid_provinces = valid_aqi_df['Province'].tolist()
    
    # In kết quả ra màn hình
    print("\n" + "="*40)
    print(f"✅ TỔNG SỐ TỈNH CÓ DỮ LIỆU AQI: {len(valid_provinces)} tỉnh")
    print("="*40)
    print("Danh sách chi tiết:")
    for prov in valid_provinces:
        print(f" - {prov}")
    print("="*40 + "\n")
    #print(df)