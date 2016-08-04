# create a polygon
# from https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html
from osgeo import ogr

# Create outer ring
outRing = ogr.Geometry(ogr.wkbLinearRing)
outRing.AddPoint(1154115.274565847, 686419.4442701361)
outRing.AddPoint(1154115.274565847, 653118.2574374934)
outRing.AddPoint(1165678.1866605144, 653118.2574374934)
outRing.AddPoint(1165678.1866605144, 686419.4442701361)
outRing.AddPoint(1154115.274565847, 686419.4442701361)

# Create inner ring
innerRing = ogr.Geometry(ogr.wkbLinearRing)
innerRing.AddPoint(1149490.1097279799, 691044.6091080031)
innerRing.AddPoint(1149490.1097279799, 648030.5761158396)
innerRing.AddPoint(1191579.1097525698, 648030.5761158396)
innerRing.AddPoint(1191579.1097525698, 691044.6091080031)
innerRing.AddPoint(1149490.1097279799, 691044.6091080031)

# Create polygon
poly = ogr.Geometry(ogr.wkbPolygon)
poly.AddGeometry(outRing)
poly.AddGeometry(innerRing)

print poly.ExportToWkt()

####
# and export it
# from http://www.gdal.org/ogr_apitut.html

import sys
from osgeo import gdal
from osgeo import ogr
import string
driverName = "KML"
drv = gdal.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
    sys.exit( 1 )
ds = drv.Create( "poly_out.kml", 0, 0, 0, gdal.GDT_Unknown )
if ds is None:
    print "Creation of output file failed.\n"
    sys.exit( 1 )
lyr = ds.CreateLayer( "point_out", None, ogr.wkbPolygon )
if lyr is None:
    print "Layer creation failed.\n"
    sys.exit( 1 )
field_defn = ogr.FieldDefn( "Name", ogr.OFTString )
field_defn.SetWidth( 32 )
if lyr.CreateField ( field_defn ) != 0:
    print "Creating Name field failed.\n"
    sys.exit( 1 )
##
feat = ogr.Feature( lyr.GetLayerDefn())
feat.SetField( "Name", "my polygon" )
feat.SetGeometry(poly)
if lyr.CreateFeature(feat) != 0:
    print "Failed to create feature in shapefile.\n"
    sys.exit( 1 )
feat.Destroy()
##
ds = None
