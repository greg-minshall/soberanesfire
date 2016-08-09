from __future__ import print_function # for eprint() below

import argparse
import os
import osgeo
from osgeo import gdal
from osgeo import ogr
from osgeo import wkt
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
    parser.add_argument('-o', '--output', type=str, required=True)
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
    if not os.access(args.output, os.W_OK):
        eprint("output file '%s' cannot be written" % args.output)
        sys.exit(2)
            
    # for first file, set base polygon to its polygon with initial color (white)
    pgons = [procfile(args.ifiles[0], args.layername, args.featurename)]
    # for each succeeding file before the last file, set the new polygon -
    # old to a new color
    for ifile in args.ifiles[1:len(args.ifiles)-1]:
        pgons = pgons + [procfile(ifile, args.layername, args.featurename)]
    # for the last file, set the last polygon - old polygon to the
    # terminal color (rust red)
    pgons = pgons + \
        [procfile(args.ifiles[len(args.ifiles)-1], args.layername, args.featurename)]

    # now write out a new KML file with the result.

    # much of this from http://www.gdal.org/ogr_apitut.html
    drv = gdal.GetDriverByName("KML");
    if drv is None:
        eprint("KML driver not found")
        sys.exit(4)
    ds = drv.Create(args.output, 0, 0, 0, gdal.GDT_Unknown)
    if ds is None:
        eprint("can't create output file %s" % args.output)
        sys.exit(2)
    layer = ds.CreateLayer("Perimeter", None, ogr.wkbMultiPolygon)
    if layer is None:
        eprint("can't create MultiPolygon layer");
        sys.exit(4)

    # need to define fields in feature before defining feature
    field_defn = ogr.FieldDefn("Name", ogr.OFTString)
    field_defn.SetWidth(32)     # XXX
    if layer.CreateField(field_defn) != 0:
        eprint("Creating name field failed")
        sys.exit(4)
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField("Name", args.featurename) # XXX
    n = len(pgons)
    # sometimes geometries are invalid:
    # https://trac.osgeo.org/geos/wiki/TopologyExceptions
    for i in range(len(pgons)):
        print(pgons[i].IsValid())
    x = pgons[1].Difference(pgons[0])
    feature.SetGeometry(x)
    if layer.CreateFeature(feature) != 0:
        eprint("failed to create feature in KML file")
        sys.exit(4)
    ds = None                   # causes gdal.Close()

def procfile(filename, layername, featurename):
    """extract the polygon of a given feature in a given layer in a given file"""
    file = ogr.Open(filename)
    # print("this is %s data" % file.GetDriver().GetName())
    # print("there is/are %d layer(s)" % file.GetLayerCount())
    l = file.GetLayerByName(layername) # type(l) == OGRLayerH
    if l is None:
        eprint("layer '%s' is not found in file '%s'" % (layername, filename))
        sys.exit(3)
    l.ResetReading()
    # find the right feature
    found = False
    for featid in range(l.GetFeatureCount()):
        feature = l.GetFeature(featid); # type(feature) == OGRFeatureH
        fieldid = feature.GetFieldIndex("Name");
        name = feature.GetFieldAsString(fieldid);
        if (name == featurename):
            found = True
            break;
    if not found:
        eprint("feature name '%s' not found in layer '%s' in file '%s'" %
               (featurename, layername, filename))
        sys.exit(3)
    # okay, we found the right feature.  now, find the polygon, maybe
    # a multigeometry
    geometry = feature.GetGeometryRef().Clone()
    return geometry

if __name__ == "__main__":
    main(sys.argv)
