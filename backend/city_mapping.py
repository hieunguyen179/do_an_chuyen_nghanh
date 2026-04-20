# backend/city_mapping.py
"""
Mapping tên tỉnh Việt Nam → Key WAQI
File này được dùng chung cho cả forecast.py và hourly_forecast.py
"""

CITY_MAPPING = {
    'hanoi': 'Hà Nội',
    '@-541225': 'Hồ Chí Minh',
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

def get_city_key(province_vn: str):
    """Tìm key WAQI từ tên tỉnh tiếng Việt"""
    for key, name in CITY_MAPPING.items():
        if name == province_vn:
            return key
    return None

def is_supported_province(province_vn: str) -> bool:
    """Kiểm tra tỉnh có được hỗ trợ API không"""
    return get_city_key(province_vn) is not None