import os

import processing

os.chdir(r'/media/j/TOSHIBA1/OneDrive - University of South Carolina - Moore School of Business/CompEcon_Fall17/Problem Sets/Problem Set 5/stadium_shapefiles')


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
