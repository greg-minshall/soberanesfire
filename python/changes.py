import osgeo
from osgeo import ogr
import zipfile
zf = zipfile.ZipFile("20160729_Soberanes_IR.kmz", "r")
print(zf)
zf.namelist()
doc = zf.open("doc.kml")
print(doc)
doc.read()

f = ogr.Open("doc.kml")
print("this is %s data" % f.GetDriver().GetName())
print("data source is %s" % f.GetName())
print("there is/are %d layer(s)" % f.GetLayerCount())
print("the first layer is named '%s'" % f.GetLayer(0).GetLayerDefn().GetName())

