# from http://stackoverflow.com/a/1206856/1527747

def main(argv):
    import argparse
    import sys
    import xml.dom.minidom

    parser = argparse.ArgumentParser(description="using xml.dom.minidom, print an xml file")
    parser.add_argument('xmlfile', type=argparse.FileType('r'),
                        nargs='?', default=sys.stdin)
    args = parser.parse_args();

    xml = xml.dom.minidom.parse(args.xmlfile)
    # (above could also be: xml.dom.minidom.parseString(xml_string))

    # the following was "toprettyxml()", but, yuck, extra blank lines,
    # etc.  "in terseness there is beauty."
    print xml.toxml()

if __name__ == "__main__":
    import sys
    main(sys.argv)
