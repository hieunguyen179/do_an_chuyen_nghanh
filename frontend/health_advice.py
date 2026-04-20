# frontend/health_advice.py
"""
Module cung cấp lời khuyên sức khỏe dựa trên chỉ số AQI
"""

def get_health_advice(aqi):
    """
    Trả về lời khuyên sức khỏe chi tiết dựa trên AQI
    
    Args:
        aqi: Chỉ số AQI (số nguyên)
    
    Returns:
        dict: {
            'title': Tiêu đề cảnh báo,
            'icon': Emoji biểu tượng,
            'advice': Danh sách lời khuyên,
            'sensitive_groups': Nhóm người nhạy cảm,
            'activities': Hướng dẫn hoạt động,
            'color': Màu chủ đạo,
            'level': Mức độ (0-5)
        }
    """
    
    if aqi <= 50:
        return {
            'title': 'Chất lượng không khí TỐT',
            'icon': '😊',
            'advice': [
                '🏃‍♂️ Tuyệt vời cho mọi hoạt động ngoài trời',
                '🪟 Mở cửa sổ để thông gió tự nhiên',
                '🚴‍♀️ Thích hợp cho chạy bộ, đạp xe, thể thao',
                '👨‍👩‍👧‍👦 An toàn cho trẻ em và người cao tuổi'
            ],
            'sensitive_groups': 'Không có nhóm nguy cơ',
            'activities': {
                '🏃 Thể thao ngoài trời': 'Rất tốt',
                '🚶 Đi bộ, tản bộ': 'Rất tốt',
                '👶 Trẻ em vui chơi': 'Rất tốt'
            },
            'color': '#00e400',
            'level': 0
        }
    
    elif aqi <= 100:
        return {
            'title': 'Chất lượng không khí TRUNG BÌNH',
            'icon': '😐',
            'advice': [
                '👴 Người nhạy cảm nên hạn chế hoạt động ngoài trời kéo dài',
                '😷 Trẻ em, người già, bệnh nhân hô hấp nên cân nhắc đeo khẩu trang',
                '🏋️‍♂️ Người bình thường vẫn có thể hoạt động bình thường',
                '⏰ Tránh tập luyện cường độ cao kéo dài (>1 giờ)'
            ],
            'sensitive_groups': 'Trẻ em, người cao tuổi, bệnh nhân hen suyễn, COPD',
            'activities': {
                '🏃 Thể thao ngoài trời': 'Tốt cho người khỏe mạnh',
                '🚶 Đi bộ, tản bộ': 'Tốt',
                '👶 Trẻ em vui chơi': 'Hạn chế thời gian'
            },
            'color': '#ffff00',
            'level': 1
        }
    
    elif aqi <= 150:
        return {
            'title': 'Chất lượng không khí KÉM',
            'icon': '😷',
            'advice': [
                '⚠️ Trẻ em, người cao tuổi, bệnh nhân hô hấp NÊN Ở TRONG NHÀ',
                '😷 Đeo khẩu trang N95/KN95 khi ra ngoài',
                '🚫 Tránh tập thể dục ngoài trời',
                '🪟 Đóng cửa sổ, bật máy lọc không khí nếu có',
                '💊 Người bệnh nên chuẩn bị sẵn thuốc'
            ],
            'sensitive_groups': 'MỌI NGƯỜI đều có thể bị ảnh hưởng. Nhóm nhạy cảm sẽ gặp vấn đề nghiêm trọng.',
            'activities': {
                '🏃 Thể thao ngoài trời': '❌ Không nên',
                '🚶 Đi bộ, tản bộ': '⚠️ Hạn chế, đeo khẩu trang',
                '👶 Trẻ em vui chơi': '❌ Ở trong nhà'
            },
            'color': '#ff7e00',
            'level': 2
        }
    
    elif aqi <= 200:
        return {
            'title': 'Chất lượng không khí XẤU',
            'icon': '😨',
            'advice': [
                '🏠 MỌI NGƯỜI nên hạn chế ra ngoài tối đa',
                '😷 BẮT BUỘC đeo khẩu trang N95/KN95 khi ra ngoài',
                '🚫 TUYỆT ĐỐI KHÔNG tập thể dục ngoài trời',
                '💊 Chuẩn bị thuốc cho người bệnh hô hấp, tim mạch',
                '🏥 Liên hệ bác sĩ nếu có triệu chứng: ho, khó thở, đau ngực',
                '🔒 Đóng kín cửa, dùng máy lọc không khí'
            ],
            'sensitive_groups': 'TẤT CẢ MỌI NGƯỜI đều chịu ảnh hưởng nghiêm trọng',
            'activities': {
                '🏃 Thể thao ngoài trời': '❌ Cấm',
                '🚶 Đi bộ, tản bộ': '❌ Tránh nếu không cần thiết',
                '👶 Trẻ em vui chơi': '❌ Ở trong nhà, đóng cửa'
            },
            'color': '#ff0000',
            'level': 3
        }
    
    elif aqi <= 300:
        return {
            'title': 'Chất lượng không khí RẤT XẤU',
            'icon': '☠️',
            'advice': [
                '🚨 TUYỆT ĐỐI KHÔNG ra ngoài nếu không cần thiết',
                '🏥 Người bệnh nên đến bệnh viện nếu có triệu chứng',
                '😷 Đeo khẩu trang chuyên dụng N99 hoặc P100',
                '📞 Gọi cấp cứu 115 nếu khó thở, đau ngực',
                '🔒 Kín cửa hoàn toàn, dán kín khe hở',
                '💨 Dùng máy lọc không khí chế độ tối đa',
                '🚗 Không mở cửa sổ xe khi di chuyển'
            ],
            'sensitive_groups': 'KHẨN CẤP: Tất cả mọi người ở trong tình trạng nguy hiểm',
            'activities': {
                '🏃 Thể thao ngoài trời': '🚨 Cấm tuyệt đối',
                '🚶 Đi bộ, tản bộ': '🚨 Chỉ khi cực kỳ cần thiết',
                '👶 Trẻ em vui chơi': '🚨 Ở trong nhà, theo dõi sát'
            },
            'color': '#99004c',
            'level': 4
        }
    
    else:  # AQI > 300
        return {
            'title': 'NGUY HIỂM - TÌNH TRẠNG KHẨN CẤP',
            'icon': '💀',
            'advice': [
                '🚨 TÌNH TRẠNG KHẨN CẤP - Ở trong nhà HOÀN TOÀN',
                '📞 Liên hệ cơ quan y tế địa phương',
                '🏥 Sẵn sàng đến bệnh viện bất cứ lúc nào',
                '😷 Đeo khẩu trang ngay cả khi ở trong nhà',
                '🚪 Kín tất cả cửa, dán kín mọi khe hở',
                '💨 Bật máy lọc không khí công suất tối đa',
                '📺 Theo dõi tin tức và chỉ đạo từ chính quyền',
                '🚗 KHÔNG di chuyển trừ trường hợp khẩn cấp'
            ],
            'sensitive_groups': '🚨 CẢ DÂN SỐ trong tình trạng nguy hiểm cực độ',
            'activities': {
                '🏃 Thể thao ngoài trời': '🚨 CẤM TUYỆT ĐỐI',
                '🚶 Đi bộ, tản bộ': '🚨 CẤM - Chỉ khẩn cấp',
                '👶 Trẻ em vui chơi': '🚨 Giám sát 24/7 trong nhà'
            },
            'color': '#7e0023',
            'level': 5
        }


def get_mask_recommendation(aqi):
    """
    Khuyến nghị loại khẩu trang phù hợp
    """
    if aqi <= 50:
        return None
    elif aqi <= 100:
        return {
            'type': 'Khẩu trang y tế thường',
            'standard': 'ASTM Level 1-2',
            'note': 'Người nhạy cảm nên đeo khi ra ngoài lâu'
        }
    elif aqi <= 150:
        return {
            'type': 'Khẩu trang N95 hoặc KN95',
            'standard': 'Lọc ≥95% hạt PM2.5',
            'note': 'Bắt buộc cho nhóm nguy cơ cao'
        }
    elif aqi <= 200:
        return {
            'type': 'Khẩu trang N95/KN95',
            'standard': 'Lọc ≥95% hạt PM2.5, kín khít',
            'note': 'BẮT BUỘC cho mọi người khi ra ngoài'
        }
    else:
        return {
            'type': 'Khẩu trang N99 hoặc P100',
            'standard': 'Lọc ≥99% hạt, có van thở',
            'note': 'Chuyên dụng, đeo cả trong nhà nếu cần'
        }