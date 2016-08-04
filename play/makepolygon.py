# create a polygon
# from https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html
from osgeo import ogr

# Create ring
ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(1179091.1646903288, 712782.8838459781)
ring.AddPoint(1161053.0218226474, 667456.2684348812)
ring.AddPoint(1214704.933941905, 641092.8288590391)
ring.AddPoint(1228580.428455506, 682719.3123998424)
ring.AddPoint(1218405.0658121984, 721108.1805541387)
ring.AddPoint(1179091.1646903288, 712782.8838459781)

# Create polygon
poly = ogr.Geometry(ogr.wkbPolygon)
poly.AddGeometry(ring)

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
