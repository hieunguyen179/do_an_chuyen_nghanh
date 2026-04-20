# frontend/components/health_card.py
"""
Component hiển thị lời khuyên sức khỏe
"""

def create_health_advice_card(advice_data):
    """
    Tạo HTML card hiển thị lời khuyên sức khỏe
    
    Args:
        advice_data: Dict từ get_health_advice()
    
    Returns:
        str: HTML string
    """
    
    # Tạo danh sách lời khuyên
    advice_items = ''.join([
        f"<li style='margin:10px 0; font-size:15px; line-height:1.6;'>{item}</li>"
        for item in advice_data['advice']
    ])
    
    # Tạo bảng hoạt động
    activity_rows = ''.join([
        f"""
        <tr>
            <td style='padding:8px; border-bottom:1px solid {advice_data['color']}33;color:#333'>{activity}</td>
            <td style='padding:8px; border-bottom:1px solid {advice_data['color']}33; text-align:right;color:#333; font-weight:bold;'>{status}</td>
        </tr>
        """
        for activity, status in advice_data['activities'].items()
    ])
    
    html = f"""<div style="background: linear-gradient(135deg, {advice_data['color']}15 0%, {advice_data['color']}30 100%); border-left: 6px solid {advice_data['color']}; border-radius: 16px; padding: 24px; margin-top: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.15);">
<div style="display:flex; align-items:center; margin-bottom:16px;color:#333;">
<span style="font-size:48px; margin-right:16px;">{advice_data['icon']}</span>
<div>
<h2 style="margin:0; color:{advice_data['color']}; font-size:24px;">{advice_data['title']}</h2>
<p style="margin:4px 0 0 0; color:{advice_data['color']}; font-size:14px;">Dựa trên chỉ số AQI hiện tại</p>
</div>
</div>
<div style="background:white; border-radius:12px; padding:20px; margin-bottom:16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);color:#333;">
<h3 style="margin:0 0 12px 0; color:{advice_data['color']}; font-size:18px;">💡 Lời khuyên sức khỏe</h3>
<ul style="margin:0; padding-left:20px;">{advice_items}</ul>
</div>
<div style="background:white; border-radius:12px; padding:20px; margin-bottom:16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
<h3 style="margin:0 0 12px 0; color:#333; font-size:18px;">👥 Nhóm nguy cơ cao</h3>
<p style="margin:0; font-size:15px; line-height:1.6; color:{advice_data['color']};">{advice_data['sensitive_groups']}</p>
</div>
<div style="background:white; border-radius:12px; padding:20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
<h3 style="margin:0 0 12px 0; color:{advice_data['color']}; font-size:18px;">🏃 Hướng dẫn hoạt động</h3>
<table style="width:100%; border-collapse:collapse; color:{advice_data['color']};">{activity_rows}</table>
</div>
</div>"""
    
    return html


def create_mask_recommendation_card(mask_data):
    """
    Tạo HTML card khuyến nghị khẩu trang
    """
    if not mask_data:
        return ""
    
    html = f"""<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 20px; margin-top: 16px; color: black; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);">
<h3 style="margin:0 0 12px 0; font-size:18px;">😷 Khuyến nghị khẩu trang</h3>
<div style="background:rgba(255,255,255,0.15); border-radius:8px; padding:16px;">
<p style="margin:0 0 8px 0; font-size:16px; font-weight:bold;">{mask_data['type']}</p>
<p style="margin:0 0 8px 0; font-size:14px;"><strong>Tiêu chuẩn:</strong> {mask_data['standard']}</p>
<p style="margin:0; font-size:14px; font-style:italic;">💡 {mask_data['note']}</p>
</div>
</div>"""
    
    return html