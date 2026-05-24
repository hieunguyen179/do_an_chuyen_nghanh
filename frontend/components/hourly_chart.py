# frontend/components/hourly_chart.py
import plotly.graph_objects as go
from backend.hourly_forecast import get_hourly_forecast

def create_hourly_chart(province_name):
    if not province_name:
        return None
        
    data = get_hourly_forecast(province_name)
    
    times = [item["display_label"] for item in data]
    aqi_values = [item["aqi"] for item in data]
    colors = [item["color"] for item in data]
    statuses = [item["status"] for item in data]
    
    fig = go.Figure()
    
    # Đường cong chính - ĐỔI MÀU LINE THÀNH XANH LÁ
    fig.add_trace(go.Scatter(
        x=times,
        y=aqi_values,
        mode='lines+markers',
        line=dict(color='#198754', width=5, shape='spline', smoothing=1.3), # Màu xanh lá
        marker=dict(
            size=16,
            color=colors,
            line=dict(width=3, color='white')
        ),
        hovertemplate='<b>%{x}</b><br>AQI: <b>%{y}</b><br>%{text}<extra></extra>',
        text=statuses,
        name=""
    ))

    # Điểm đầu tiên to hơn + viền đen
    with fig.batch_update():
        new_sizes = [20 if i == 0 else 16 for i in range(len(aqi_values))]
        new_line_widths = [5 if i == 0 else 3 for i in range(len(aqi_values))]
        new_line_colors = ['black' if i == 0 else 'white' for i in range(len(aqi_values))]
        
        fig.data[0].marker.size = new_sizes
        fig.data[0].marker.line.width = new_line_widths
        fig.data[0].marker.line.color = new_line_colors

    fig.update_layout(
        title={
            'text': f"Dự báo 24 giờ của tỉnh: <b>{province_name}</b>",
            'x': 0.5,
            'xanchor': 'center',
            'font': dict(size=24, color="#333333") # ĐỔI CHỮ THÀNH MÀU ĐEN XÁM
        },
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="#ffffff", # ĐỔI NỀN THÀNH MÀU TRẮNG
        height=350,
        margin=dict(l=40, r=40, t=60, b=80),
        xaxis=dict(
            tickfont=dict(size=14, color="#333333"), # ĐỔI CHỮ TRỤC X THÀNH MÀU ĐEN XÁM
            gridcolor="rgba(0,0,0,0)",  # ✅ BỎ LINE NGANG
            zeroline=False
        ),
        yaxis=dict(
            range=[0, max(max(aqi_values), 100) * 1.2],
            showgrid=False,  # ✅ BỎ GRIDLINE
            gridcolor="rgba(0,0,0,0)",
            showticklabels=False,  # ✅ BỎ SỐ BÊN TRÁI
            tickfont=dict(color="rgba(0,0,0,0)"),
            title=dict(
                text="",  # ✅ BỎ CHỮ "AQI"
                font=dict(color="rgba(0,0,0,0)", size=16)
            )
        ),
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),
        showlegend=False
    )

    # ✅ DÙNG EMOJI THAY VÌ TEXT
    icon_map = {
        "Tốt": "😊",
        "Trung bình": "😐", 
        "Kém": "😷",
        "Xấu": "😵",
        "Rất xấu": "🤮",
        "Nguy hại": "💀"
    }
    
    for i, item in enumerate(data):
        # Icon
        fig.add_annotation(
            x=times[i],
            y=-12,
            text=icon_map.get(item["status"], "😐"),
            showarrow=False,
            font=dict(size=28),
            yshift=0,
            xref="x",
            yref="y"
        )
        # Label trạng thái
        fig.add_annotation(
            x=times[i],
            y=-25,
            text=item["status"],
            showarrow=False,
            font=dict(size=11, color="white"),
            bgcolor=item["color"],
            bordercolor="white",
            borderwidth=2,
            borderpad=4,
            opacity=0.9,
            xref="x",
            yref="y"
        )
    
    return fig