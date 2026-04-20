# frontend/components/forecast_bar.py
import base64
from pathlib import Path
from backend.forecast import get_forecast

IMG_DIR = Path(__file__).parent.parent / "static" / "img"
ICONS = {
    'Tốt': 'Smile_ljng.png',
    'Trung bình': 'Bad_ljng.png',
    'Kém': 'Horror_ljng.png',
    'Xấu': 'Reject_ljng.png',
    'Rất xấu': 'Alert_gemini-removebg-preview.png',
}

def get_icon_base64(status):
    file = IMG_DIR / ICONS.get(status, ICONS['Tốt'])
    if file.exists():
        return base64.b64encode(file.read_bytes()).decode()
    return None

def create_forecast_bar(province_name, current_aqi=None):
    if not province_name:
        return "<div></div>"
        
    # get_forecast bây giờ tự động lấy AQI từ file GeoJSON, không cần truyền current_aqi nữa
    data = get_forecast(province_name)
    
    cards = []
    for item in data:
        icon_b64 = get_icon_base64(item["status"])
        icon_html = f'<img src="data:image/png;base64,{icon_b64}" width="100" height="100" style="margin:10px 0;">' if icon_b64 else "Icon"

        cards.append(f"""
        <div class="forecast-card">
            <div class="day-label">{item['day']}</div>
            <div class="icon">{icon_html}</div>
            <div class="date">{item['date']}</div>
            <div class="aqi-value" style="color:{item['color']}">{item['aqi']}</div>
            <div class="status" style="background:{item['color']}">{item['status']}</div>
        </div>
        """)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            html, body {{
                width: 100%;
                height: 100%;
                overflow: hidden;
                margin: 0;
                padding: 0;
            }}

            .forecast-container {{
                margin-top : 20px;
                width: 100%;
                height: 450px;
                background: linear-gradient(135deg, #569156 0%, #000000 100%);
                border-radius: 28px;
                padding: 28px 32px;
                box-sizing: border-box;
                color: white;
                border: 2px solid white;
                font-family: 'Segoe UI', Tahoma, sans-serif;
                box-shadow: 0 20px 50px rgba(0,0,0,0.3);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }}

            .forecast-title {{
                font-size: 26px;
                font-weight: 700;
                text-align: center;
                margin: 0 0 8px 0;
                text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            }}

            .forecast-subtitle {{
                font-size: 14px;
                text-align: center;
                opacity: 0.9;
                margin-bottom: 24px;
                font-weight: 500;
            }}

            .forecast-grid {{
                display: flex;
                justify-content: space-between;
                align-items: stretch;
                gap: 20px;
                flex: 1;
                padding: 0 10px;
            }}

            .forecast-card {{
                flex: 1;
                background: white;
                border-radius: 24px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
                transition: all 0.35s ease;
                min-width: 0;
                border: 4px solid transparent;
                position: relative;
                overflow: hidden;
            }}

            .forecast-card::before {{
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0; height: 6px;
                background: linear-gradient(90deg, var(--card-color), var(--card-color));
                opacity: 0.8;
            }}

            .forecast-card:hover {{
                transform: translateY(-12px) scale(1.05);
                box-shadow: 0 25px 50px rgba(0,0,0,0.35);
                z-index: 10;
            }}

            .day-label {{
                font-size: 17px;
                font-weight: 700;
                color: #444;
                margin-bottom: 8px;
            }}

            .icon img {{
                filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
            }}

            .date {{
                font-size: 15px;
                color: #666;
                margin: 8px 0;
                font-weight: 600;
            }}

            .aqi-value {{
                font-size: 42px;
                font-weight: 900;
                margin: 12px 0;
                text-shadow: 0 3px 10px rgba(0,0,0,0.2);
            }}

            .status {{
                font-size: 15px;
                font-weight: bold;
                color: white;
                padding: 8px 20px;
                border-radius: 30px;
                min-width: 100px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="forecast-container">
            <div class="forecast-title">
                Dự báo chất lượng không khí 5 ngày tới · <strong>{province_name}</strong>
            </div>
            <div class="forecast-subtitle">
                Dữ liệu dự báo từ WAQI + mô hình nội suy xu hướng
            </div>
            <div class="forecast-grid">
                {''.join(cards)}
            </div>
        </div>
    </body>
    </html>
    """