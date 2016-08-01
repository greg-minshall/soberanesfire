#!/bin/bash

# get all the VIIR (?) IR files into place and unzipped

for i in `ls ~/Downloads/20160[78]*Soberanes_IR.kmz | sed sX/Users/minshall/Downloads/XX | sed sX.kmzXX`; do
    if [ ! -e $i ]; then
        mkdir $i;
    fi
    if [ ! -e $i/$i.kmz ]; then
        cp -p ~/Downloads/$i.kmz $i;
    fi
    if [ ! -e $i/doc.kml ]; then
        (cd $i; unzip $i.kmz doc.kml)
    fi
    if grep -H Sobranes $i/doc.kml; then
        echo fixing up $i/doc.kml
        (echo g/Sobranes/s/Sobranes/Soberanes/; echo wq) | ed $i/doc.kml
    fi
    if grep -H Sorberanes $i/doc.kml; then
        echo fixing up $i/doc.kml
        (echo g/Sorberanes/s/Sorberanes/Soberanes/; echo wq) | ed $i/doc.kml
    fi
done
