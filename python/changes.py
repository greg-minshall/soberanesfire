import osgeo
from osgeo import ogr

# it would be nice to read direct from a .kmz (zip) file.  but it
# doesn't seem like the current gdal/ogr supports that.
# import zipfile
# zf = zipfile.ZipFile("20160729_Soberanes_IR.kmz", "r")
# print(zf)
# zf.namelist()
# ndoc = zf.open("doc.kml")
# data = doc.read()

f = ogr.Open("doc.kml")
print("this is %s data" % f.GetDriver().GetName())
print("data source is %s" % f.GetName())
print("there is/are %d layer(s)" % f.GetLayerCount())
print("the first layer is named '%s'" % f.GetLayer(0).GetLayerDefn().GetName())
print(f.GetLayerByName("Soberanes").GetName())

l = f.GetLayerByName("Soberanes")

hpfid = -1
for featid in range(l.GetFeatureCount()):
    feature = l.GetFeature(featid);
    fieldid = feature.GetFieldIndex("Name");
    print(feature.GetFieldAsString(fieldid));
