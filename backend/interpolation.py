# backend/interpolation.py
import geopandas as gpd
import pandas as pd
import numpy as np

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

def calculate_missing_aqi(gdf_with_some_aqi, centroids_path="data/centroids/vn_provinces_centroids.geojson"):
    # Đọc centroids và chuyển sang EPSG:4326 (nếu chưa)
    centroids = gpd.read_file(centroids_path)
    if centroids.crs is None:
        centroids = centroids.set_crs("EPSG:4326")
    elif centroids.crs.to_epsg() != 4326:
        centroids = centroids.to_crs("EPSG:4326")

    # Tạo DataFrame chứa tâm tỉnh có tên
    centroid_points = gpd.GeoDataFrame(
        {"NAME_1": centroids["NAME_1"]},
        geometry=centroids.geometry.centroid,
        crs="EPSG:4326"
    )
    centroid_points["lon"] = centroid_points.geometry.x
    centroid_points["lat"] = centroid_points.geometry.y

    # Gán tọa độ cho các tỉnh có AQI thật
    valid_provinces = gdf_with_some_aqi.dropna(subset=["AQI"]).copy()
    valid_provinces = valid_provinces.merge(
        centroid_points[["NAME_1", "lat", "lon"]],
        on="NAME_1",
        how="left"
    )
    valid_provinces = valid_provinces.dropna(subset=["lat", "lon"])  # an toàn

    # Bắt đầu với gdf gốc
    result_gdf = gdf_with_some_aqi.copy()
    result_gdf["AQI_source"] = "Trạm đo"

    # Nội suy cho các tỉnh thiếu
    missing_mask = result_gdf["AQI"].isna()
    for idx in result_gdf[missing_mask].index:
        province_name = result_gdf.loc[idx, "NAME_1"]
        
        # Lấy tâm tỉnh cần nội suy
        target_row = centroid_points[centroid_points["NAME_1"] == province_name]
        if target_row.empty:
            result_gdf.loc[idx, "AQI_source"] = "Không nội suy được"
            continue
            
        target_lat = target_row["lat"].iloc[0]
        target_lon = target_row["lon"].iloc[0]

        # Tính khoảng cách đến tất cả trạm có dữ liệu
        distances = valid_provinces.apply(
            lambda row: haversine_distance(target_lat, target_lon, row["lat"], row["lon"]),
            axis=1
        )
        distances = np.array(distances)
        distances = np.where(distances == 0, 0.001, distances)  # tránh chia 0

        weights = 1.0 / (distances ** 2)
        interpolated_aqi = np.sum(weights * valid_provinces["AQI"]) / np.sum(weights)

        result_gdf.loc[idx, "AQI"] = round(interpolated_aqi)
        result_gdf.loc[idx, "AQI_source"] = "Nội suy (IDW)"

    result_gdf["AQI"] = pd.to_numeric(result_gdf["AQI"], errors="coerce")
    return result_gdf