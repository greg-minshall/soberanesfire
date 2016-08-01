from __future__ import print_function # for eprint() below

import argparse
import os
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
    # use "type=str" since we use the file name for ogr.Open()
    parser.add_argument('ifiles', type=str, nargs='+')
    args = parser.parse_args();

    # make sure ifiles are all readable
    badfile = False
    for ifile in args.ifiles:
        if not os.access(ifile, os.R_OK):
            eprint("input file '%s' cannot be read" % ifile)
            badfile = True
    if badfile:
        sys.exit(2)
            
    # for first file, set base polygon to its polygon with initial color (white)
    procfile(args.ifiles[0], args.layername, args.featurename)
    # for each succeeding file before the last file, set the new polygon -
    # old to a new color
    for ifile in args.ifiles[1:len(args.ifiles)-1]:
        print(ifile)
    # for the last file, set the last polygon - old polygon to the
    # terminal color (rust red)
    print(args.ifiles[len(args.ifiles)-1])

    # now write out a new KML file with the result.

def procfile(filename, lname, fname):
    """extract the polygon of a given feature in a given layer in a given file"""
    file = ogr.Open(filename)
    # print("this is %s data" % file.GetDriver().GetName())
    # print("there is/are %d layer(s)" % file.GetLayerCount())
    l = file.GetLayerByName(lname) # type(l) == OGRLayerH
    if l is None:
        eprint("layer '%s' is not found in file '%s'" % (lname, filename))
        sys.exit(3)
    # find the field
    fid = -1
    for featid in range(l.GetFeatureCount()):
        feature = l.GetFeature(featid); # type(feature) == OGRFeatureH
        fieldid = feature.GetFieldIndex("Name");
        name = feature.GetFieldAsString(fieldid);
        if (name == fname):
            fid = fieldid;
            break;
    if fid == -1:
        eprint("feature name '%s' not found in layer '%s' in file '%s'" %
               (fname, lname, filename))
        sys.exit(3)

if __name__ == "__main__":
    main(sys.argv)
