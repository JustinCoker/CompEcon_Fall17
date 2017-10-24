'''
This script uses shapefiles generated in qgis by running
qgis_stadium_nocrime.py in the python terminal of QGIS.

This script generates a python figure showing Nationals Stadium with a 400m
ring.
'''

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np
import os

exec(open("./plot_shape.py").read())

# setup Lambert Conformal basemap.
# set resolution=None to skip processing of boundary datasets.
fig = plt.figure(figsize=(24, 12))

ax = fig.add_subplot(111)

map = Basemap(resolution= 'f',projection= 'lcc', epsg= 4326,llcrnrlon=-77.01969,
              llcrnrlat= 38.85883, urcrnrlon=-76.99192, urcrnrlat=38.88070,
              lat_0= 38.87300, lon_0= -77.00734)
map.drawcoastlines()
map.drawmapboundary(fill_color='black')
map.fillcontinents(color='white', lake_color='blue')

os.chdir((r"/media/j/TOSHIBA1/OneDrive - University of South Carolina - "
         r"Moore School of Business/CompEcon_Fall17/Problem Sets/Problem Set 5"
         r"/stadium_shapefiles"))

files = [s for s in os.listdir(os.getcwd()) if ".shp" in s]

for el in files:
    map.readshapefile(el[:-4], el[:-4])


plot_shape(map.roads_info, map.roads, 'None', '#fcca7e', .2, 3, 1)

plot_shape(map.buildings_info, map.buildings, '#a7a7a7', 'black', .1, 3, 1)

plot_shape(map.water_info, map.water, 'blue', 'black', .1, 3, 1)

plot_shape(map.radius4_info, map.radius4, 'pink', 'black', .1, 3, .65)

map.plot(-77.00748, 38.87296, marker = 'o', zorder = 5)

plt.show()
