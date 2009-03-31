#!/bin/sh
## mkvdts2ac3 - add an ac3 track to mkv from its dts
## Author: Jake Wharton
## Version: 0.2-080311

## Used to time execution
START=$(date +%s)

## Path to file
DEST=$(dirname "$1")

## File name without the extension
NAME=$(basename "$1" .mkv)

## Working Directory
## I personally use the current directory since my temp partition
## is tiny (WD=.). To use the directory the file is in use $DEST.
WD=.

## Get the track number for the DTS track
DTSTRACK=$(mkvmerge -i "$1" | grep DTS | cut -d: -f1 | cut -d" " -f3)

## Setup temporary files
DTSFILE="$WD/$NAME.dts"
AC3FILE="$WD/$NAME.ac3"
DSTFILE="$WD/$NAME.ac3.mkv"

## Extract the DTS track
mkvextract tracks "$1" $DTSTRACK:"$DTSFILE"

## Convert DTS to AC3
dcadec -o wavall "$DTSFILE" | aften - "$AC3FILE"

## Delete extracted DTS file
rm -f "$DTSFILE"

## Remux AC3 into original file (retaining DTS)
mkvmerge -o "$DSTFILE" "$1" "$AC3FILE"

## Delete our temporary AC3 file
rm -f "$AC3FILE"

## Move the newly created file over the old one
mv "$DSTFILE" "$1"

## Display total execution time
END=$(date +%s)
echo "Total processing time: $(($END - $START)) seconds."