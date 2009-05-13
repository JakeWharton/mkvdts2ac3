#!/bin/bash
## mkvdtsextract
##   removes the main DTS audio track
## Author: Jake Wharton <jakewharton@gmail.com>
## Version: 1.0

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
DTSTRACK=$(mkvmerge -i "$1" | grep A_DTS | cut -d: -f1 | cut -d" " -f3)
KEEPTRACKS=$(mkvmerge -i "$1" | grep audio | grep -v A_DTS | cut -d: -f1 | cut -d" " -f3 | awk '{ if (T == "") T=$1; else T=T","$1 } END { print T}' )

## Setup temporary files
DTSFILE="$WD/$NAME.dts"
NEWFILE="$WD/$NAME.new.mkv"

## Extract the DTS track
mkvextract tracks "$1" $DTSTRACK:"$DTSFILE"

## Remove DTS track from MKV
mkvmerge -o "$NEWFILE" -a $KEEPTRACKS "$1"

## Move new file over the old one (NOT SAFELY)
mv "$NEWFILE" "$1"

## Display total execution time
END=$(date +%s)
echo "Total processing time: $(($END - $START)) seconds."