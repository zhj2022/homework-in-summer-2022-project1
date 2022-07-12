import numpy as np
import pandas as pd
import xlrd
from SpatialRegion import SpatialRegion

xstep = 5
ystep = 5

poi = pd.read_excel('shanghai_poi.xls')
poi_loca = poi[['lng', 'lat']]  #两列分别经/纬
"""索引方式:poi_loca['lng'][0]"""

taxi_points = np.load('arrive_point_array.npy', allow_pickle=True)  #三列分别为经/纬/时
"""索引方式:taxi_points[0][0]"""

minlat = min(sorted(poi_loca['lat'])[0], sorted(taxi_points[:, 1])[0])
minlng = min(sorted(poi_loca['lng'])[0], sorted(taxi_points[:, 0])[0])
maxlat = max(sorted(poi_loca['lat'], reverse=True)[0], sorted(taxi_points[:, 1], reverse=True)[0])
maxlng = max(sorted(poi_loca['lng'], reverse=True)[0], sorted(taxi_points[:, 0], reverse=True)[0])

shanghai_spatial_region = SpatialRegion(minlat, minlng, maxlat, maxlng, xstep=xstep, ystep=ystep)

from_region_to_poi = {}
from_region_to_taxi = {}
poi_vector = []
for i in range(poi_loca.shape[0]):
    poi_vector.append([])
    for j in range(24):
        poi_vector[i].append(0)
poi_vector = np.array(poi_vector)  #初始化用于聚类的poi向量

for i in range(poi_loca.shape[0]):
    if shanghai_spatial_region.coord2cell(poi_loca['lat'][i], poi_loca['lng'][i]) not in from_region_to_poi.keys():
        from_region_to_poi[shanghai_spatial_region.coord2cell(poi_loca['lat'][i], poi_loca['lng'][i])] = []
    else:
        from_region_to_poi[shanghai_spatial_region.coord2cell(poi_loca['lat'][i], poi_loca['lng'][i])].append(i)

for i in range(taxi_points.shape[0]):
    if shanghai_spatial_region.coord2cell(taxi_points[i][1], taxi_points[i][0]) not in from_region_to_taxi.keys():
        from_region_to_taxi[shanghai_spatial_region.coord2cell(taxi_points[i][1], taxi_points[i][0])] = []
    else:
        from_region_to_taxi[shanghai_spatial_region.coord2cell(taxi_points[i][1], taxi_points[i][0])].append(i)

"""遍历有poi分布的每个区域，将每个区域中的车流与poi关联，并填入poi_vector中
"""
for region, poi_list in from_region_to_poi.items():
    for poi_num in poi_list:
        if region in from_region_to_taxi.keys():
            for taxi_num in from_region_to_taxi[region]:
                poi_vector[poi_num][taxi_points[taxi_num][2]] += 1

np.save('poi_vector(step=5km).npy', poi_vector)


# R=0.1
# for i in range(poi_loca.shape[0]):
#     for j in range(taxi_points.shape[0]):
#         print(get_distance(poi_loca['lng'][i], poi_loca['lat'][i], taxi_points[j][0], taxi_points[j][1]), i)
#         if get_distance(poi_loca['lng'][i], poi_loca['lat'][i], taxi_points[j][0], taxi_points[j][1]) <= R:
#             poi_vector[i][taxi_points[j][2]] += 1
# 逐一计算距离的代码，运行时间过长

for i in range(poi_vector.shape[0]):
    print(poi_vector[i])
