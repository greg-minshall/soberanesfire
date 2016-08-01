from __future__ import print_function # for eprint() below

import argparse
import osgeo
from osgeo import ogr
import sys

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
# get feature name: Heat Perimeter

# from [[http://stackoverflow.com/a/14981125][stack exchange]]
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main(argv):
    cmd = argv[0];
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--layername', type=str, required=True,
                        help="name of desired layer")
    parser.add_argument('-f', '--featurename', type=str, required=True,
                        help="name of desired feature (within layer)")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        required=True)
    parser.add_argument('files', type=argparse.FileType('r'))
    args = parser.parse_args();
    if args.layername is None:
        eprint("missing layername")
        usage(cmd)

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

if __name__ == "__main__":
    main(sys.argv)
