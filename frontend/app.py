# frontend/app.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium
from frontend.visualize import create_map
import geopandas as gpd
import config
import pandas as pd
import urllib.parse # Thư viện để mã hóa URL (quan trọng)
from textwrap import dedent
from frontend.components.forecast_bar import create_forecast_bar
from frontend.components.hourly_chart import create_hourly_chart
from frontend.utils import find_nearest_province
from frontend.health_advice import get_health_advice , get_mask_recommendation
from frontend.components.health_card import create_health_advice_card , create_mask_recommendation_card

# =================================================================
# 1. CẤU HÌNH TRANG
# =================================================================
st.set_page_config(page_title="AirWatch VN", layout="wide")

# =================================================================
# 2. CSS (ĐÃ ĐỔI TÔNG TRẮNG & XANH LÁ)
# =================================================================
st.markdown("""
<style>
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
[data-testid="stHeader"], footer { display: none; }
iframe { 
    height: 800px !important; 
    border-radius: 12px !important; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

/* CSS CHO TIÊU ĐỀ SIDEBAR (Xanh lá chủ đạo) */
.sidebar-title-box {
    background-color: #198754; /* Xanh lá đậm */
    border: 1px solid #146c43;
    border-radius: 8px;
    padding: 10px 16px; 
    margin-bottom: 16px; 
    box-shadow: 0 4px 12px rgba(25,135,84,0.2);
    height: 40px; 
    display: flex;
    align-items: center;
    justify-content: center;
}
.sidebar-title-box h3 {
    color: #ffffff; /* Chữ trắng */
    margin: 0; 
    font-size: 1.25rem; 
}

/* CSS CHO DANH SÁCH CUỘN (Nền trắng) */
.right-sidebar-list {
    margin-top :10px;
    height: 800px !important; 
    max-height: 800px !important;
    overflow-y: auto !important; 
    overflow-x: hidden !important;
    background-color: #ffffff !important; /* Trắng */
    border-radius: 12px !important;
    padding: 16px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    border: 1px solid #e9ecef;
}

/* Style cho các link <a> (thay cho st.button) */
.province-item {
    width: 100%;
    padding: 12px;
    margin: 6px 0;
    background: #f8f9fa; /* Xám rất nhạt */
    border: 1px solid #dee2e6; /* Xám viền */
    border-radius: 8px;
    color: #333333; /* Chữ đen xám */
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
    display: block; 
}

.right-sidebar-list a {
    text-decoration: none;
}

.province-item:hover {
    background: #e8f5e9; /* Xanh lá cực nhạt khi hover */
    border-color: #198754; /* Viền xanh lá */
    transform: translateX(4px);
    color: #0f5132; /* Chữ xanh lá thẫm */
}
.aqi-highlight {
    font-weight: bold;
    font-size: 16px;
    float: right; 
    text-shadow: 0px 0px 1px rgba(0,0,0,0.2); /* Thêm bóng nhẹ để số vàng/xanh dễ đọc trên nền trắng */
}

.bg-img {
    margin-top: 24px;
    width: 100%;
    height: 400px;
    background-origin : border-box;
    border-radius: 16px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    color: white;
    border : 2px solid white;
    padding: 40px 50px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    font-family: 'Segoe UI', sans-serif;
    position: relative;
    overflow: hidden;
}  
            
/* CSS cho ô tìm kiếm */
div[data-testid="stTextInput"] {
    margin-bottom: 12px;
}

div[data-testid="stTextInput"] > div > div > input {
    background-color: #ffffff !important; /* Trắng */
    border: 2px solid #ced4da !important; /* Xám nhạt */
    border-radius: 8px !important;
    color: #333333 !important; /* Chữ đen xám */
    padding: 12px 16px !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #198754 !important; /* Xanh lá focus */
    box-shadow: 0 0 0 3px rgba(25, 135, 84, 0.2) !important;
    outline: none !important;
}

div[data-testid="stTextInput"] > div > div > input::placeholder {
    color: #adb5bd !important; /* Xám chữ mờ */
    font-style: italic !important;
}

/* Điều chỉnh chiều cao list khi có search box */
.right-sidebar-list {
    margin-top: 10px;
    height: calc(800px - 100px) !important; 
    max-height: calc(800px - 100px) !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    background-color: #ffffff !important;
    border-radius: 12px !important;
    padding: 16px !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    border: 1px solid #e9ecef;
}
            
/* Animation cho nút định vị */
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(25, 135, 84, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(25, 135, 84, 0); }
    100% { box-shadow: 0 0 0 0 rgba(25, 135, 84, 0); }
}

.locate-button-container button:active {
    animation: pulse 1s;
}
                  
</style>
""", unsafe_allow_html=True)

# =================== LOAD DATA ===================================
@st.cache_data(ttl=3600)  # Cache 1 giờ
def load_data():
    gdf = gpd.read_file(config.DATA_PATH)
    gdf['AQI'] = pd.to_numeric(gdf['AQI'], errors='coerce')
    return gdf

gdf = load_data()  # DÙNG CHUNG CHO TOÀN BỘ APP
# ==================== TẠO SESSION STATE ==========================
if 'selected_province' not in st.session_state:
    st.session_state.selected_province = None

# ==================== TIÊU ĐỀ ====================================
st.title("AirWatch – Giám sát chất lượng không khí Việt Nam")

# ============ XỬ LÝ QUERY KHI CLICK VÀO TỈNH ======================
if "province" in st.query_params:
    clicked_province = urllib.parse.unquote(st.query_params["province"])

    if clicked_province == "None":
        st.session_state.selected_province = None
    else:
        st.session_state.selected_province = clicked_province

    st.query_params.clear()

# ===== Canh bao Nguong~ =======
if st.session_state.selected_province:
    selected_data = gdf[gdf['NAME_1'] == st.session_state.selected_province]

    if not selected_data.empty:
        current_aqi = selected_data.iloc[0]['AQI']
        province = selected_data.iloc[0]['NAME_1']
        
        if not pd.isna(current_aqi):
            aqi_value = int(current_aqi)
            
            # CẢNH BÁO CHỈ KHI AQI > 150
            if aqi_value > 150:
                
                # XÁC ĐỊNH MỨC ĐỘ CẢNH BÁO
                if aqi_value <= 200:
                    alert_level = "XẤU"
                    alert_color = "#ff0000"
                    alert_icon = "😨"
                    alert_action = "Hạn chế ra ngoài và đeo khẩu trang N95 khi cần thiết"
                elif aqi_value <= 300:
                    alert_level = "RẤT XẤU"
                    alert_color = "#99004c"
                    alert_icon = "☠️"
                    alert_action = "TUYỆT ĐỐI KHÔNG ra ngoài nếu không cần thiết. Đeo khẩu trang N99"
                else:
                    alert_level = "NGUY HIỂM"
                    alert_color = "#7e0023"
                    alert_icon = "💀"
                    alert_action = "TÌNH TRẠNG KHẨN CẤP - Ở trong nhà hoàn toàn. Liên hệ cơ quan y tế"
                
                # HIỂN THỊ BANNER CẢNH BÁO
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {alert_color} 0%, {alert_color}dd 100%);
                    border: 3px solid {alert_color};
                    border-radius: 12px;
                    padding: 20px 24px;
                    margin-bottom: 20px;
                    box-shadow: 0 8px 24px {alert_color}66;
                    animation: pulse_alert 2s infinite;
                ">
                    <div style="display:flex; align-items:center; gap:16px;">
                        <span style="font-size:48px;">{alert_icon}</span>
                        <div style="flex:1;">
                            <h2 style="
                                margin:0 0 8px 0; 
                                color:white; 
                                font-size:24px; 
                                font-weight:bold;
                            ">
                                🚨 CẢNH BÁO: Chất lượng không khí tại {province} đang ở mức {alert_level}!
                            </h2>
                            <p style="
                                margin:0; 
                                color:white; 
                                font-size:16px; 
                                line-height:1.6;
                            ">
                                <strong>AQI hiện tại: {aqi_value}</strong><br>
                                👉 {alert_action}
                            </p>
                        </div>
                    </div>
                </div>
                
                <style>
                @keyframes pulse_alert {{
                    0%, 100% {{
                        box-shadow: 0 8px 24px {alert_color}66;
                    }}
                    50% {{
                        box-shadow: 0 8px 32px {alert_color}99, 0 0 20px {alert_color}66;
                    }}
                }}
                </style>
                """, unsafe_allow_html=True)

# Ket thuc canh bao

col1, col2 = st.columns([3, 1])

with col1:
    # NÚT CẬP NHẬT
    if st.button("Cập nhật dữ liệu AQI", type="primary", use_container_width=True):
        with st.spinner("Đang lấy dữ liệu mới..."):
            try:
                from backend.data_processing import process_data
                process_data()
                st.success("✅ Cập nhật thành công!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")

    # Xử lý state của bản đồ
    if 'selected_province' not in st.session_state:
        st.session_state.selected_province = None
    
    if "province" in st.query_params:
        clicked_province = urllib.parse.unquote(st.query_params["province"])
        
        if clicked_province == "None":
            st.session_state.selected_province = None
        else:
            st.session_state.selected_province = clicked_province
        
        st.query_params.clear()
    
    # BẢN ĐỒ
    m = create_map(st.session_state.selected_province)
    st_folium(m, width=None, height=800, returned_objects=[])

    #========================================================
    # =================================================================
with col2:
    # ===== 1. TITLE BAR =====
    st.markdown('<div class="sidebar-title-box"><h3>Danh sách tỉnh</h3></div>', unsafe_allow_html=True)
    
    # ===== 2. Ô TÌM KIẾM =====
    search_query = st.text_input(
        label="Tìm kiếm tỉnh",
        placeholder="Nhập tên tỉnh...",
        key="province_search",
        label_visibility="collapsed"
    )

    # ===== 3. LỌC DỮ LIỆU THEO TÌM KIẾM =====
    provinces = gdf.sort_values('AQI', ascending=False).dropna(subset=['AQI'])
    
    if search_query:
        provinces = provinces[
            provinces['NAME_1'].str.contains(search_query, case=False, na=False)
        ]

    if search_query and len(provinces) == 1:
        auto_select = provinces.iloc[0]['NAME_1']
        if st.session_state.selected_province != auto_select:
            st.session_state.selected_province = auto_select
            st.rerun()
    
    # ===== 4. HIỂN THỊ DANH SÁCH =====
    html_list_content = '<div class="right-sidebar-list">'
    
    if provinces.empty:
        html_list_content += """
        <div style="text-align:center; padding:40px; color:#999;">
            <p style="font-size:18px;">❌ Không tìm thấy tỉnh nào</p>
            <p style="font-size:14px; margin-top:10px;">Thử tìm kiếm với từ khóa khác</p>
        </div>
        """
    else:
        for _, row in provinces.iterrows():
            province = row['NAME_1']
            aqi = row['AQI']
            
            aqi_str = f"{int(aqi)}"
            if aqi <= 50:
                color = "#00e400"
            elif aqi <= 100:
                color = "#cccc16" # Vàng sẫm hơn một chút cho dễ nhìn trên nền trắng
            elif aqi <= 150:
                color = "#ff7e00"
            elif aqi <= 200:
                color = "#ff0000"
            else:
                color = "#99004c"
            
            province_url_encoded = urllib.parse.quote(province)
            
            html_list_content += dedent(f"""
            <a href="?province={province_url_encoded}" target="_self" class="province-item">
                {province}
                <span class='aqi-highlight' style='color: {color};'>{aqi_str}</span>
            </a>
            """)
    
    html_list_content += f'<hr><a href="?province=None" target="_self" class="province-item" style="text-align: center; color:#dc3545;">🗑️ Ẩn đánh dấu</a>'
    html_list_content += '</div>'
    
    st.markdown(html_list_content, unsafe_allow_html=True)

# =========================================================

# =================================================================
# THANH THÔNG TIN – DÙNG ẢNH LOCAL
# =================================================================
import base64
from pathlib import Path

def img_to_base64(img_path):
    if img_path.exists():
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

IMG_DIR = Path(__file__).parent / "static" / "province"

PROVINCE_IMAGES = {
    "An Giang" : "angiang.png",
    "Bắc Giang": "bacgiang.png",
    "Bắc Kạn": "backan.png",
    "Bạc Liêu": "baclieu.png",
    "Bà Rịa - Vũng Tàu": "bariavungtau.png",
    "Bến Tre": "bentre.png",
    "Bình Định": "binhdinh.png",
    "Bình Dương": "binhduong.png",
    "Bình Phước": "binhphuoc.png",
    "Bình Thuận": "binhthuan.png",
    "Cà Mau": "camau.png",
    "Cần Thơ": "cantho.png",
    "Cao Bằng": "caobang.png",
    "Đắk Lắk": "daklak.png",
    "Đắk Nông": "daknong.png",
    "Đà Nẵng": "danang.png",
    "Điện Biên": "dienbien.png",
    "Đồng Nai": "dongnai.png",
    "Đồng Tháp": "dongthap.png",
    "Gia Lai": "gialai.png",
    "Hà Giang": "hagiang.png",
    "Hải Dương": "haiduong.png",
    "Hải Phòng": "haiphong.png",
    "Hà Nam": "hanam.png",
    "Hà Tĩnh": "hatinh.png",
    "Hậu Giang": "haugiang.png",
    "Hòa Bình": "hoabinh.png",
    "Thừa Thiên Huế": "hue.png",
    "Hưng Yên": "hungyen.png",
    "Khánh Hòa": "khanhhoa.png",
    "Kiên Giang": "kiengiang.png",
    "Kon Tum": "kontum.png",
    "Lai Châu": "laichau.png",
    "Lâm Đồng": "lamdong.png",
    "Lạng Sơn": "langson.png",
    "Lào Cai": "laocai.png",
    "Long An": "longan.png",
    "Nam Định": "namdinh.png",
    "Nghệ An": "nghean.png",
    "Ninh Bình": "ninhbinh.png",
    "Ninh Thuận": "ninhthuan.png",
    "Phú Thọ": "phutho.png",
    "Phú Yên": "phuyen.png",
    "Quảng Bình": "quangbinh.png",
    "Quảng Nam": "quangnam.png",
    "Quảng Ngãi": "quangngai.png",
    "Quảng Ninh": "quangninh.png",
    "Quảng Trị": "quangtri.png",
    "Sóc Trăng": "soctrang.png",
    "Sơn La": "sonla.png",
    "Tam Đảo": "tamdao.png",
    "Tây Ninh": "tayninh.png",
    "Thái Bình": "thaibinh.png",
    "Thái Nguyên": "thainguyen.png",
    "Thanh Hóa": "thanhhoa.png",
    "Tiền Giang": "tiengiang.png",
    "Trà Vinh": "travinh.png",
    "Tuyên Quang": "tuyernquang.png",
    "Vĩnh Long": "vinhlong.png",
    "Yên Bái": "yenbai.png",
    "Hà Nội": "hanoi.png",
    "Hồ Chí Minh": "hochiminh.png",
    "Đà Nẵng": "danang.png",
    "Thừa Thiên Huế": "hue.png",
    "Hải Phòng": "haiphong.png",
    "Cần Thơ": "cantho.png",
}

current_aqi_value = None

if st.session_state.selected_province:
    selected_data = gdf[gdf['NAME_1'] == st.session_state.selected_province]
    
    if selected_data.empty:
        st.warning(f"Không tìm thấy dữ liệu cho tỉnh: {st.session_state.selected_province}")
        st.session_state.selected_province = None
    else:
        row = selected_data.iloc[0]
        province = row['NAME_1']
        aqi_raw = row['AQI']
        update_date = row.get('Date', 'Không rõ')

        if pd.isna(aqi_raw):
            aqi_display = "N/A"
            status = "Chưa có dữ liệu"
            status_color = "#999999"
            current_aqi_value = None
        else:
            aqi = int(aqi_raw)
            current_aqi_value = aqi  
            aqi_display = str(aqi)
            if aqi <= 50:
                status, status_color = "Tốt", "#00e400"
            elif aqi <= 100:
                status, status_color = "Trung bình", "#cccc16"
            elif aqi <= 150:
                status, status_color = "Kém", "#ff7e00"
            elif aqi <= 200:
                status, status_color = "Xấu", "#ff0000"
            else:
                status, status_color = "Rất xấu", "#99004c"

        filename = PROVINCE_IMAGES.get(province)
        img_path = IMG_DIR / filename if filename else None
        encoded = img_to_base64(img_path) if img_path else None
        bg_image = f"data:image/png;base64,{encoded}" if encoded else "https://i.imgur.com/2f8p8vP.jpg"  

        st.markdown(f"""
        <div class="bg-img" 
                 style="background: linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.85)), 
                                    url('{bg_image}') center /cover no-repeat;">
            <div style="position: absolute; top: 20px; right: 30px; opacity: 0.9; font-size: 14px; color: white;">
                Cập nhật: {update_date}
            </div>
            <h1 style="margin:0; font-size: 58px; font-weight: bold; text-shadow: 0 4px 15px rgba(0,0,0,0.8); color: white;">
                {province}
            </h1>
            <h2 style="margin: -10px 0px 20px; font-size: 40px; font-weight: bold; color: {status_color}; 
                text-shadow: 0 4px 15px rgba(0,0,0,0.9);">
                {aqi_display} AQI - Tình Trạng : {status}
            </h2>
            <div style="font-size: 15px; font-weight: bold; color: #333;">
                <span style="background: rgba(255, 255, 255, 0.85); 
                        padding: 12px 16px; border-radius: 80px; 
                        backdrop-filter: blur(10px); 
                        box-shadow: 0 8px 25px rgba(0,0,0,0.3);">
                    🌿 Cuộn xuống để biết thêm chi tiết ▼
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    # GRADIENT XANH LÁ CHO BANNER CHƯA CHỌN TỈNH
    st.markdown("""
    <div style="
        margin-top: 24px;
        width: 100%;
        height: 400px;
        background: linear-gradient(135deg, #0f5132 0%, #198754 50%, #28a745 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 8px 30px rgba(25, 135, 84, 0.3);
    ">
        Chọn một tỉnh từ bản đồ hoặc danh sách bên phải để xem chi tiết
    </div>
    """, unsafe_allow_html=True)

if st.session_state.selected_province and current_aqi_value:
    advice = get_health_advice(current_aqi_value)
    mask_rec = get_mask_recommendation(current_aqi_value)
    
    health_card_html = create_health_advice_card(advice)
    st.html(health_card_html)
    
    if mask_rec:
        mask_card_html = create_mask_recommendation_card(mask_rec)
        st.html(mask_card_html)

if st.session_state.selected_province:
    forecast_html = create_forecast_bar(st.session_state.selected_province, current_aqi=current_aqi_value)
    components.html(forecast_html, height=450, scrolling=False)
else:
    # GRADIENT XANH LÁ CHO BANNER DỰ BÁO
    st.markdown("""
    <div style="
        margin-top: 24px;
        width: 100%;
        height: 450px;
        background: linear-gradient(135deg, #0f5132 0%, #198754 50%, #28a745 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 8px 30px rgba(25, 135, 84, 0.3);
    ">
        Dự báo 5 ngày tiếp theo ! 
    </div>
    """, unsafe_allow_html=True)

st.markdown("""   
    <style>
        div[data-testid="stPlotlyChart"] {
            margin-top: 12px !important;
        }
    </style>
    """, unsafe_allow_html=True)

if st.session_state.selected_province:
    chart = create_hourly_chart(st.session_state.selected_province)
    if chart:
        st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
else:
    # GRADIENT XANH LÁ CHO BANNER BIỂU ĐỒ 24H
    st.markdown("""
    <div style="margin-top:10px; margin-bottom : 10px ; 
            width:100% ; height:350px; 
            background: linear-gradient(135deg, #0f5132 0%, #198754 50%, #28a745 100%); 
            border-radius: 16px; display: flex; 
            align-items: center; 
            justify-content: center; 
            color: white; 
            font-size: 32px; 
            font-weight: bold; 
            text-align: center; 
            box-shadow: 0 8px 30px rgba(25, 135, 84, 0.3);">          
        Dự báo 24 giờ
    </div>
    """, unsafe_allow_html=True)

# =============== 3 THẺ THỐNG KÊ (TRẮNG + CHỮ ĐEN XÁM) ==================
st.markdown(f"""
<div style="display:flex; gap:20px; margin-bottom:20px;margin-top:20px;">
    <div style="flex:1; background:#ffffff; padding:20px; border-radius:12px;border:1px solid #dee2e6; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h4 style="color:#333333; margin-top:0;">🌍 Trung bình toàn quốc</h4>
        <h2 style="color:#cccc16; margin-bottom:0; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">{int(gdf['AQI'].mean())}</h2>
    </div>
    <div style="flex:1; background:#ffffff; padding:20px; border-radius:12px;border:1px solid #dee2e6; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h4 style="color:#333333; margin-top:0;">🏆 Tỉnh tốt nhất</h4>
        <h2 style="color:#00e400; margin-bottom:0; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">{gdf.sort_values('AQI').iloc[0]['NAME_1']}</h2>
    </div>
    <div style="flex:1; background:#ffffff; padding:20px; border-radius:12px;border:1px solid #dee2e6; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h4 style="color:#333333; margin-top:0;">⚠️ Tỉnh tệ nhất</h4>
        <h2 style="color:#ff0000; margin-bottom:0; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">{gdf.sort_values('AQI', ascending=False).iloc[0]['NAME_1']}</h2>
    </div>
</div>
""", unsafe_allow_html=True)