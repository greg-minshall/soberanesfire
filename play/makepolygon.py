# create a polygon
# from https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html
from osgeo import ogr

poly = ogr.Geometry(ogr.wkbMultiPolygon)

# Create ring #1
ring1 = ogr.Geometry(ogr.wkbLinearRing)
ring1.AddPoint(1204067.0548148106, 634617.5980860253)
ring1.AddPoint(1204067.0548148106, 620742.1035724243)
ring1.AddPoint(1215167.4504256917, 620742.1035724243)
ring1.AddPoint(1215167.4504256917, 634617.5980860253)
ring1.AddPoint(1204067.0548148106, 634617.5980860253)

# Create polygon #1
poly1 = ogr.Geometry(ogr.wkbPolygon)
poly1.AddGeometry(ring1)
poly.AddGeometry(poly1)

# Create ring #2
ring2 = ogr.Geometry(ogr.wkbLinearRing)
ring2.AddPoint(1179553.6811741155, 647105.5431482664)
ring2.AddPoint(1179553.6811741155, 626292.3013778647)
ring2.AddPoint(1194354.20865529, 626292.3013778647)
ring2.AddPoint(1194354.20865529, 647105.5431482664)
ring2.AddPoint(1179553.6811741155, 647105.5431482664)

# Create polygon #2
poly2 = ogr.Geometry(ogr.wkbPolygon)
poly2.AddGeometry(ring2)
poly.AddGeometry(poly2)

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
