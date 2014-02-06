#! /bin/sh

echo "$SHELL"

./indexwithloctime.py "$1" "$2"
./matchimage2loc.py "$2"/pending "$2"
./mergeperloctime.py "$2" "$3"
./sortimages.py "$3"
