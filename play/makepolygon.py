# create a polygon
# from https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html
from osgeo import ogr

# Create a geometry collection
poly =  ogr.Geometry(ogr.wkbGeometryCollection)

# Add a point
point = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(-122.23, 47.09)
poly.AddGeometry(point)

# Add a line
line = ogr.Geometry(ogr.wkbLineString)
line.AddPoint(-122.60, 47.14)
line.AddPoint(-122.48, 47.23)
poly.AddGeometry(line)

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
