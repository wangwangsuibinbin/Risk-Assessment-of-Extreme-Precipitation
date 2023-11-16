import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import basefunc
import fiona.transform
import rasterio.sample
import numpy as np
import tqdm
def reproject_coords(src_crs, dst_crs, coords):
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    xs, ys = fiona.transform.transform(src_crs, dst_crs, xs, ys)
    return [[x,y] for x,y in zip(xs, ys)]
# 输入表格
#data = pd.read_csv('lv.csv')

# 初始化网格数组  
grid = np.zeros((720, 1440)) 

ss = -178.5
se = 178.5

# 生成经度坐标,从-180到180,分割成100000份
lons = np.linspace(ss, se, 130000)

# 生成纬度坐标,从-90到90,分割成50000份
lats = np.linspace(-60, 75, 60000)


with rasterio.open(r"D:\QQ\PhD\gpkg\tow\lv (1).tif") as dataset:
    src_crs = 'EPSG:4326'
    dst_crs = dataset.crs.to_proj4()  # '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m no_defs'
    #dst_crs = dataset.crs.to_wkt()  # 'PROJCS["World_Mollweide",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS    84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mollweide"],PARAMETER["central_meridian",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
    #coords = [[135.456, 30.567]]  # [longitude, latitude] not [lat, lon]...
    aaa = -178.5 +30
    for lon in tqdm.tqdm(lons):
        for lat in lats:
            new_coords = reproject_coords(src_crs, dst_crs, [[lon, lat]])
            #print(new_coords)
            values = list(rasterio.sample.sample_gen(dataset, new_coords))
            #print(values[0][0])
            if values[0][0]>0:
                print(lon,lat,values[0][0])
                # 计算网格索引
                lon_idx = int((lon) / 0.25)
                lat_idx = int((90 - lat) / 0.25)
                
                # 更新该网格路段总长
                grid[lat_idx, lon_idx] += values[0][0]

        # grid数组最后保存了每个网格的路段总长度
        #plt.imshow(grid)
        if lon>aaa:
            aaa += 30
            ref_tif=r'./data/ref.tif'
            basefunc.array2Raster(grid[:600,],ref_tif,f'./LV_{ss}-{se}_{lon}.tif')
