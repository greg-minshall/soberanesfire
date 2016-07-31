import sys
import osgeo
from osgeo import ogr

# XXX
# it would be nice to read direct from a .kmz (zip) file.  but it
# doesn't seem like the current gdal/ogr supports that.
# import zipfile
# zf = zipfile.ZipFile("20160729_Soberanes_IR.kmz", "r")
# print(zf)
# zf.namelist()
# ndoc = zf.open("doc.kml")
# data = doc.read()
# XXX

# get layer name: Soberanes
alname = "Soberanes"
# get feature name: Heat Perimeter
afname = "Heat Perimeter"

# from [[http://stackoverflow.com/a/14981125][stack exchange]]
from __future__ import print_function
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def usage(cmd):
    print "usage: %s [{-l|--layername} name] [{-f|--featurename} name]
{-o|--output} filename infile1 [infile2 [infile3 [ ... ]]]"
    sys.exit(1)


def main(argv):
    opts, args = getopt(argv[1:], "f:l:o:", ["featurename", "layername", "output"])
    except getopt.GetoptError:
        usage(argv[0])
    for opt, arg in opts:
        if opt in ["f", "featurename"]:
            afname = arg
        elif opt in ["l", "layername"]:
            alname = arg
        elif opt in ["o", "output"]:
            aoname = arg

# for first file, set base polygon to its polygon with initial color (white)

# for each succeeding file before the last file, set the new polygon -
# old to a new color

# for the last file, set the last polygon - old polygon to the
# terminal color (rust red)

# now write out a new KML file with the result.


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
    name = feature.GetFieldAsString(fieldid);
    if (name == "Heat Perimeter"):
        print("success")
