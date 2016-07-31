import osgeo
import zipfile
zf = zipfile.ZipFile("20160729_Soberanes_IR.kmz", "r")
print(zf)
zf.namelist()
doc = zf.open("doc.kml")
print(doc)
doc.read()
