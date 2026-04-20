# frontend/visualize.py
import folium
import geopandas as gpd
import config
import pandas as pd
from pathlib import Path
import base64  # <-- 1. IMPORT THÊM BASE64

# === CẤU HÌNH ẢNH ===
IMG_DIR = Path(__file__).parent / "static" / "img"

# 2. SỬA LẠI TÊN FILE CHO KHỚP VỚI THƯ MỤC CỦA BẠN
ICONS = {
    'Tốt': 'Smile_ljng.png',
    'Trung bình': 'Bad_ljng.png',
    'Kém': 'Horror_ljng.png',
    'Xấu': 'Reject_ljng.png',
    'Rất xấu': 'Alert_gemini-removebg-preview.png',
}

# 3. SỬA HÀM NÀY ĐỂ MÃ HÓA BASE64
def get_icon_url(status):
    filename = ICONS.get(status)
    if not filename:
        return None
    
    path = IMG_DIR / filename
    
    if not path.exists():
        print(f"Cảnh báo: Không tìm thấy file icon: {path}")
        return None
    
    # Đọc file ảnh dưới dạng binary
    with open(path, "rb") as f:
        data = f.read()
    
    # Mã hóa sang Base64
    encoded = base64.b64encode(data).decode("utf-8")
    
    # Trả về một data URL
    return f"data:image/png;base64,{encoded}"

# === TRẠNG THÁI & MÀU SẮC ===
def get_aqi_status(aqi):
    if pd.isna(aqi):
        return 'Chưa có dữ liệu'
    aqi = float(aqi)
    if aqi <= 50:  return 'Tốt'
    if aqi <= 100: return 'Trung bình'
    if aqi <= 150: return 'Kém'
    if aqi <= 200: return 'Xấu'
    if aqi <= 300: return 'Rất xấu'
    return 'Nguy hại'

def get_color(aqi):
    if pd.isna(aqi): return '#ffffff'
    aqi = float(aqi)
    if aqi <= 50:  return '#00e400'
    if aqi <= 100: return "#cccc16"
    if aqi <= 150: return '#ff7e00'
    if aqi <= 200: return '#ff0000'
    if aqi <= 300: return '#99004c'
    return '#4d0000'

# === TẠO POPUP ===
# (Hàm này của bạn đã đúng, không cần sửa)
def create_popup_html(row):
    province = row['NAME_1']
    aqi = row['AQI']
    date = row['Date']
    status = get_aqi_status(aqi)
    color = get_color(aqi)

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 270px;max-height:270px; padding: 8px;">
        <h4 style="margin: 0 0 6px; color: #222;font-weight:bold; font-size: 13px;">{province}</h4>
        <p style="margin: 3px 0; font-size:13px;"><b>AQI:</b> 
            <span style="font-size: 1.3em; color: {color};">
                {aqi if not pd.isna(aqi) else 'Chưa có dữ liệu'}
            </span>
        </p>
        <p style="margin: 3px 0;font-size:13px;"><b>Cập nhật:</b> {date}</p>
        <p style="margin: 6px 0 3px;font-size:13px;"><b>Tình trạng:</b> 
            <span style="font-weight: bold;font-size:13px; color: {color};">{status}</span>
        </p>
    """

    # === THÊM ẢNH + THÔNG BÁO ===
    icon_url = get_icon_url(status)
    if icon_url:
        if status == 'Tốt':
            html += """
            <hr style="border: 0; border-top: 1px dashed #aaa; margin: 10px 0;">
            <p style="margin: 8px 0; color: #2e8b57; font-weight: bold; text-align: center; font-size: 10px;">
                Chất lượng không khí bây giờ khá tốt
            </p>
            """
        elif status == 'Trung bình':
            html += """
            <hr style="border: 0; border-top: 1px dashed #aaa; margin: 10px 0;">
            <p style="margin: 8px 0; color: #ff8c00; font-weight: bold; text-align: center; font-size: 10px;">
                Chất lượng không khí ở mức trung bình
            </p>
            """
        elif status == 'Kém':
            html += """
            <hr style="border: 0; border-top: 1px dashed #aaa; margin: 10px 0;">
            <p style="margin: 8px 0; color: #ff4500; font-weight: bold; text-align: center; font-size: 10px;">
                Chất lượng không khí kém, mang theo khẩu trang khi ra ngoài
            </p>
            """
        elif status == 'Xấu':
            html += """
            <hr style="border: 0; border-top: 1px dashed #aaa; margin: 10px 0;">
            <p style="margin: 8px 0; color: #b22222; font-weight: bold; text-align: center; font-size: 10px;">
                Chất lượng không khí xấu, luôn đeo khẩu trang khi ra ngoài
            </p>
            """
        elif status == 'Rất xấu':
            html += """
            <hr style="border: 0; border-top: 1px dashed #aaa; margin: 10px 0;">
            <p style="margin: 8px 0; color: #8b0000; font-weight: bold; text-align: center; font-size: 10px;">
                Chất lượng không khí rất xấu, tránh ra ngoài
            </p>
            """
        html += f"""
        <div style="text-align: center; margin: 10px 0; background: transparent;">
            <img src="{icon_url}" width="120" height="120" 
                 style="background:transparent;">
        </div>
        """

    html += "</div>"
    return html

# === TẠO BẢN ĐỒ ===
# (Hàm này của bạn đã đúng, không cần sửa)
# === TẠO BẢN ĐỒ ===
def create_map(selected_province=None):  # THÊM THAM SỐ
    gdf = gpd.read_file(config.DATA_PATH)
    m = folium.Map(location=[16.0, 107.0], zoom_start=7, tiles=None, bgcolor='#e6f2ff')


    for _, row in gdf.iterrows():
        source = row.get('AQI_source' ,'Trạm đo')

        aqi = row['AQI']
        province = row['NAME_1']
        geojson = row['geometry'].__geo_interface__
        popup = folium.Popup(create_popup_html(row), max_width=1000)

        # ĐÁNH DẤU TỈNH ĐƯỢC CHỌN
        is_selected = (province == selected_province)
        
        if is_selected:
            line_weight = 6.0
            fill_opacity = 0.85
            border_color = "#000000"

        else:
            line_weight = 1.0 if source == "Nội suy (IDW)" else 1.0
            fill_opacity = 0.65
            border_color = "#000000" if source == "Nội suy (IDW)" else "#444444"

        folium.GeoJson(
            geojson,
            style_function=lambda x, aqi=aqi, lw=line_weight , fo=fill_opacity, bc=border_color: {
                'fillColor': get_color(aqi),
                'color': bc,
                'weight': lw,
                'fillOpacity': fo,
            },
            popup=popup,
            tooltip=folium.Tooltip(
                f"<b>{province}</b><br>"
                f"AQI: <b>{int(aqi) if not pd.isna(aqi) else 'N/A'}</b><br>"
                f"Nguồn: <i>{source}</i>",
                style="font-family: Arial; font-size: 13px; background: rgba(255,255,255,0.9); padding: 6px; border-radius: 6px;"
            )
        ).add_to(m)

        # ZOOM + MỞ POPUP KHI CHỌN
        if is_selected:
            bounds = row['geometry'].bounds
            m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

        centroid = row['geometry'].centroid
        lat = centroid.y
        lon = centroid.x
        
        # Tạo label cho tên tỉnh
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(html=f"""
                <div style="
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                    font-weight: bold;
                    color: #000;
                    text-align: center;
                    white-space: nowrap;
                    text-shadow: 
                        -1px -1px 0 #fff,
                        1px -1px 0 #fff,
                        -1px 1px 0 #fff,
                        1px 1px 0 #fff,
                        0 0 3px #fff;
                ">
                    {province}
                </div>
            """)
        ).add_to(m)

    # === LEGEND ===
    # (Legend của bạn đã đúng, không cần sửa)
    legend_html = '''
    <div style="position: fixed; bottom: 20px; left: 20px; z-index: 1000; 
                background: white; padding: 12px; border: 1px solid #333; border-radius: 8px; 
                font-family: Arial; font-size: 13px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
        <p style="margin:0 0 8px ;color:#000; font-weight:bold;font-size:10px;">Chỉ số AQI</p>
        <p style="margin:3px 0;color:#00e400;display:flex;line-height:20px;align-items:center;justify-content:flex-start;">
            <i style="background:#00e400; width:18px;margin-right:10px ;height:18px; display:inline-block; border-radius:3px;"></i>
            0-50: Tốt
        </p>
        <p style="margin:3px 0;color:#cccc16;display:flex;line-height:20px;align-items:center;justify-content:flex-start;">
            <i style="background:#ffff00; width:18px;margin-right:10px ;height:18px; display:inline-block; border-radius:3px;"></i>
            51-100: Trung bình
        </p>
        <p style="margin:3px 0;color:#ff7e00;display:flex;line-height:20px;align-items:center;justify-content:flex-start;">
            <i style="background:#ff7e00; width:18px;margin-right:10px ;height:18px; display:inline-block; border-radius:3px;"></i>
            101-150: Kém
        </p>
        <p style="margin:3px 0;color:#ff0000;display:flex;line-height:20px;align-items:center;justify-content:flex-start;">
            <i style="background:#ff0000; width:18px;margin-right:10px ;height:18px; display:inline-block; border-radius:3px;"></i>
            151-200: Xấu
        </p>
        <p style="margin:3px 0;color:#99004c;display:flex;line-height:20px;align-items:center;justify-content:flex-start;">
            <i style="background:#99004c; width:18px;margin-right:10px ;height:18px; display:inline-block; border-radius:3px;"></i>
            201-300: Rất xấu
        </p>
        <p style="margin:3px 0;color:#999;display:flex;line-height:20px;align-items:center;justify-content:flex-start;">
            <i style="background:#ffffff; width:18px;margin-right:10px ;height:18px; display:inline-block; border:1px solid #ccc; border-radius:3px;line-height:25px;"></i>
            Chưa có dữ liệu
        </p>
    </div>
    '''
    # =======================
    
    m.get_root().html.add_child(folium.Element(legend_html))
    return m