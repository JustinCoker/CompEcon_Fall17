'''
This script uses Washginton DC crime map shapefiles and OpenStreetMap
shapefiles to map crime in Washinton DC's Ward 1.

Due to the size of spatially referenced data, the shapefiles have been left
out of the repository.

'''

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os
# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
plt.figure(figsize=(36, 18))

map = Basemap(resolution= 'h',projection= 'aea',llcrnrlon=-77.051325,
              llcrnrlat= 38.913931, urcrnrlon=-77.0121, urcrnrlat=38.938311
              lat_0= 38.926139, lon_0= -77.031688)

map.drawcoastlines()
map.drawmapboundary(fill_color= 'aqua') #fills map with aqua
map.fillcontinents(color='white', lake_color='aqua') #fills continents with coral and lakes with aqua

os.chdir(os.environ['data_dir'])
os.chdir('Ward_from_2012')


map.readshapefile('Ward_from_2012', 'ward_shapefile', drawbounds = False)

os.chdir(os.environ['data_dir'])
os.chdir('geofabrik')


map.readshapefile('roads_free_1', 'roads')

map.readshapefile('buildings_a_free_1', 'buildings')

map.readshapefile('water_a_free_1', 'water1')

map.readshapefile('waterways_free_1', 'water2')


os.chdir(os.environ['data_dir'])
os.chdir('test_crime_shapefile')


map.readshapefile('latlon', 'crime')

for info, shape in zip(map.ward_shapefile_info, map.ward_shapefile):
    if info['WARD'] == 1:
        x, y = zip(*shape)
        map.plot(x, y, marker=None,color='m')



for info, crime in zip(map.crime_info, map.crime):
    map.plot(crime[0], crime[1], marker='o', color='r', markersize=7*.6*map.crime.count(crime))
plt.show()
