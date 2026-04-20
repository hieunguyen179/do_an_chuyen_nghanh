# frontend/utils.py
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Tính khoảng cách giữa 2 điểm trên Trái Đất (km)
    Sử dụng công thức Haversine
    """
    R = 6371.0  # Bán kính Trái Đất (km)
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def find_nearest_province(user_lat, user_lon, gdf):
    """
    Tìm tỉnh gần nhất với vị trí người dùng
    
    Args:
        user_lat: Vĩ độ người dùng
        user_lon: Kinh độ người dùng
        gdf: GeoDataFrame chứa dữ liệu các tỉnh
    
    Returns:
        Tên tỉnh gần nhất
    """
    min_distance = float('inf')
    nearest_province = None
    
    for _, row in gdf.iterrows():
        # Lấy tâm tỉnh (centroid)
        centroid = row['geometry'].centroid
        province_lat = centroid.y
        province_lon = centroid.x
        
        # Tính khoảng cách
        distance = haversine_distance(user_lat, user_lon, province_lat, province_lon)
        
        if distance < min_distance:
            min_distance = distance
            nearest_province = row['NAME_1']
    
    return nearest_province, min_distance