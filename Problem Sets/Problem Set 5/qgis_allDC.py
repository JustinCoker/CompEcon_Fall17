'''
This script must be run inside the python terminal of QGIS.

This generates a crime heatmap of the district including Ward boundaries.
'''


import os

import processing

os.chdir(r'/media/j/TOSHIBA1/OneDrive - University of South Carolina - Moore School of Business/CompEcon_Fall17/Problem Sets/Problem Set 5/ALL_DC_shapefiles')


pt_layer = QgsVectorLayer("Point?crs=EPSG:4326", "Point", "memory")
QgsMapLayerRegistry.instance().addMapLayer(pt_layer)

pt_layer.startEditing()

fet = QgsFeature()

fet.setGeometry( QgsGeometry.fromPoint(QgsPoint(-77.00741, 38.87296)) )

pt_layer.addFeatures([fet])

buff_list = [.004, .007]

for el in buff_list:

    processing.runalg('qgis:fixeddistancebuffer', "Point", el, 30, True,
                      "radius" + str(el)[-1:] + ".shp")


files = os.listdir(os.getcwd())

shape = [s for s in files if ".shp" in s if "radius" not in s]

radius = [s for s in files if ".shp" in s if "radius" in s]

for s in shape:
    layer = iface.addVectorLayer(s, s[:-4], "ogr")
    if s[:-4]+str('.qml') in os.listdir(os.getcwd()):
        layer.loadNamedStyle(s[:-4]+str('.qml'))

radius.sort()
radius.reverse()

transp = 75
for r in radius:
    transp = transp-8
    layer = iface.addVectorLayer(r, r[:-4], "ogr")
    layer.setLayerTransparency(transp)

canvas = qgis.utils.iface.mapCanvas()
canvas.zoomToSelected(layer=pt_layer)
for i in range(4):
    canvas.zoomIn()

csv = (r"file:////media/j/TOSHIBA1/OneDrive - University of South Carolina - "
       r"Moore School of Business/CompEcon_Fall17/Problem Sets/Problem Set 5/"
       r"ALL_DC_shapefiles/Crime_Incidents_in_2016.csv?delimiter=%s&xField=%s"
       r"&yField=%s")
uri = csv % (",", "LONGITUDE", "LATITUDE")
crime = QgsVectorLayer(uri, 'crime', 'delimitedtext')
QgsMapLayerRegistry.instance().addMapLayer(crime)
crime.loadNamedStyle('crime.qml')

canvas = qgis.utils.iface
canvas.setActiveLayer(crime)
canvas.zoomToActiveLayer()

canvas.mapCanvas().zoomScale(42000)

c = iface.activeComposers()[0].composition()

image = c.printPageAsRaster(0)

image.save('output.png','png')
