#!/bin/bash
# mkvdts2ac3 - add an ac3 track to mkv from its dts
# Author: Jake Wharton <jakewharton@gmail.com>
# Website: http://mine.jakewharton.com/projects/show/mkvdts2ac3
# Version: 0.3.2b
# License:
#   Copyright 2009 Jake Wharton
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Version display function
displayversion() {
	echo "mkvdts2ac3-0.3.2b - by Jake Wharton <jakewharton@gmail.com>"
	echo ""
}
# Help display function
displayhelp() {
	echo "Usage: $0 [options] <filename>"
	echo "Options:"
	echo "     -v, --version    Print script version information"
	echo "     -h, --help       Print command usage"
	echo ""
	echo "     -n, --no-dts     Do not retain the DTS track"
	echo "     -k, --keep-dts   Keep external DTS track (implies '-n')"
	echo "     -d, --default    Mark AC3 track as default"
	echo "     -t TRACKID,"
	echo "     --track TRACKID  Specify alternate DTS track"
	echo "     -e, --external   Leave AC3 track out of file. Does not modify the"
	echo "                      original matroska file. This overrides '-n' and"
	echo "                      '-d' arguments."
	echo ""
}

# Used to time execution
START=$(date +%s)

# Display version header
displayversion

# Parse arguments and/or filename
while [ -z $MKVFILE ]; do
	
	# If we're out of arguments no filename was passed
	if [ $# -eq 0 ]; then
		echo "ERROR: You must supply a filename."
		echo ""
		displayhelp
		exit
	fi
	
	case "$1" in
	
		"-e" | "--external" )
			EXTERNAL=1
			# Don't allow -d or -n switches if they're already set
			NODTS=0
			KEEPDTS=0
			DEFAULT=0
		;;
		
		"-n" | "--no-dts" )
			# Only allow this if we aren't making the file external
			if [ -z $EXTERNAL ]; then
				NODTS=1
			fi
		;;
		
		"-k" | "--keep-dts" )
			# Only allow external DTS track if muxing AC3 track
			if [ -z $EXTERNAL ]; then
				KEEPDTS=1
			fi
			
		;;
		
		"-t" | "--track" )
			# Move required TRACKID argument "up"
			shift
			DTSTRACK=$1
		;;
		
		"-d" | "--default" )
			# Only allow this if we aren't making the file external
			if [ -z $EXTERNAL ]; then
				DEFAULT=1
			fi
		;;
		
		"-v" | "--version" )
			# Version information is always displayed so just exit here
			exit
		;;
		
		"-h" | "--help" )
			displayhelp
			exit
		;;
		
		-* | --* )
			echo "ERROR: Invalid argument '$1'."
			echo ""
			displayhelp
			exit
		;;
		
		* )
			MKVFILE=$1
			shift
			
			# Ensure there are no arguments after the filename
			if [ $# -ne 0 ]; then
				echo "ERROR: You cannot supply any arguments after the filename. Please check the command syntax below against what has been parsed."
				echo "PARSED (if blank using respective default):"
				echo "  Strip DTS: $NODTS"
				echo "  Keep DTS: $KEEPDTS"
				echo "  AC3 default: $DEFAULT"
				echo "  External AC3: $EXTERNAL"
				echo "  DTS track: $DTSTRACK"
				echo "  MKV file: $MKVFILE"
				echo ""
				displayhelp
				exit
			fi
		;;
	esac 
	
	# Move arguments "up" one spot
	shift
done

# Check the file exists and we have permissions
if [ ! -e "$MKVFILE" -o ! -f "$MKVFILE" ]; then
	echo "ERROR: '$MKVFILE' is not a file."
	exit
elif [ ! -r "$MKVFILE" -o ! -w "$MKVFILE" ]; then
	echo "ERROR: Cannot read '$MKVFILE'."
	exit
elif [ -z $EXTERNAL -a ! -w "$MKVFILE" ]; then
	# Only check write permission if we're not keeping the AC3 external
	echo "ERROR: Cannot write '$MKVFILE'."
	exit
fi

# Check dependencies (mkvtoolnix, libdca, aften)
if [ -z "$(which mkvmerge)" -o ! -x "$(which mkvmerge)" ]; then
	echo "ERROR: The program 'mkvmerge' is not in the path. Is mkvtoolnix installed?"
	exit
elif [ -z "$(which mkvextract)" -o ! -x "$(which mkvextract)" ]; then
	echo "ERROR: The program 'mkvextract' is not in the path. Is mkvtoolnix installed?"
	exit
elif [ -z "$(which mkvinfo)" -o ! -x "$(which mkvinfo)" ]; then
	echo "ERROR: The program 'mkvinfo' is not in the path. Is mkvtoolnix installed?"
	exit
elif [ -z "$(which dcadec)" -o ! -x "$(which dcadec)" ]; then
	echo "ERROR: The program 'dcadec' is not in the path. Is libdca installed?"
	exit
elif [ -z "$(which aften)" -o ! -x "$(which aften)" ]; then
	echo "ERROR: The program 'aften' is not in the path. Is aften installed?"
	exit
fi

# Path to file
DEST=$(dirname "$MKVFILE")

# File name without the extension
NAME=$(basename "$MKVFILE" .mkv)

# Working Directory
# I personally use the current directory since my temp partition
# is tiny (WD="."). To use the directory the file is in use $DEST.
WD="/tmp"

# If the track id wasn't specified via command line then search for the first DTS audio track
if [ -z $DTSTRACK ]; then
	DTSTRACK=$(mkvmerge -i "$MKVFILE" | grep -m 1 "audio (A_DTS)" | cut -d: -f1 | cut -d" " -f3)
	
	# Check to make sure there is a DTS track in the MVK
	if [ -z $DTSTRACK ]; then
		echo "ERROR: There are no DTS tracks in '$MKVFILE'."
		exit
	fi
else
	# Checks to make sure the command line argument track id is valid
	VALID=$(mkvmerge -i "$MKVFILE" | grep "Track ID $DTSTRACK: audio (A_DTS)")
	
	if [ -z $VALID ]; then
		echo "ERROR: Track ID '$DTSTRACK' is not a DTS track and/or does not exist."
		exit
	else
		echo "INFO: Using alternate DTS track with ID '$DTSTRACK'"
	fi
fi

# Get the language for the DTS track specified
DTSLANG=$(mkvinfo "$MKVFILE" | grep -A 12 "Track number: $DTSTRACK" | tail -n 1 | cut -d" " -f5)

# Setup temporary files
DTSFILE="$WD/$NAME.dts"
AC3FILE="$WD/$NAME.ac3"
NEWFILE="$WD/$NAME.new.mkv"

# Extract the DTS track
mkvextract tracks "$MKVFILE" $DTSTRACK:"$DTSFILE"

# Check to make sure the extraction completed successfully
if [ $? -ne 0 ]; then
	echo "ERROR: Extracting the DTS track failed."
	exit
fi

# Convert DTS to AC3
dcadec -o wavall "$DTSFILE" | aften - "$AC3FILE"

# Check to make sure the conversion completed successfully
if [ $? -ne 0 ]; then
	echo "ERROR: Converting the DTS to AC3 failed."
	
	rm -f "$DTSFILE" #clean up
	rm -f "$AC3FILE" #clean up
	exit
fi

# Remove DTS file unless explicitly keeping DTS track
if [ -z $KEEPDTS ]; then
	rm -f "$DTSFILE"

	if [ $? -ne 0 ]; then
		echo "WARNING: Could not delete temporary file '$DTSFILE'. Please do this manually after the script has completed."
	fi
fi

# Check there is enough free space for AC3+MKV
MKVFILESIZE=$(du "$MKVFILE" | awk '{print $1}')
AC3FILESIZE=$(du "$AC3FILE" | awk '{print $1}')
WDFREESPACE=$(df "$WD" | tail -n 1 | awk '{print $4}')
if [ $(($MKVFILESIZE + $AC3FILESIZE)) -gt $WDFREESPACE ]; then
	echo "ERROR: There is not enough free space on '$WD' to create the new file."
	
	rm -f "$AC3FILE" #clean up
	exit
fi

if [ $EXTERNAL ]; then
	# We need to trick the rest of the script so that there isn't a lot of
	# code duplication. Basically $NEWFILE will be the AC3 track and we'll
	# change $MKVFILE to where we want the AC3 track to be so we don't
	# overwrite the MKV file only an AC3 track
	NEWFILE=$AC3FILE
	MKVFILE="$DEST/$NAME.ac3"
else
	# Start to "build" command
	CMD="mkvmerge -o \"$NEWFILE\""
	
	# If user doesn't want the original DTS track drop it
	if [ $NODTS ]; then
		# Count the number of audio tracks in the file
		AUDIOTRACKS=$(mkvmerge -i "$MKVFILE" | grep "audio (A_" | wc -l) #)#<-PN2 highlighting fix
		
		if [ $AUDIOTRACKS -eq 1 ]; then
			# If there is only the DTS audio track then drop all audio tracks
			CMD="$CMD -A"
		else
			# Get a list of all the other audio tracks
			SAVETRACKS=$(mkvmerge -i "$MKVFILE" | grep "audio (A_" | cut -d: -f1 | grep -vx "Track ID $DTSTRACK" | cut -d" " -f3 | awk '{ if (T == "") T=$1; else T=T","$1 } END { print T }') #)#<-Fix PN2 highlight
			# And copy only those
			CMD="$CMD -a \"$SAVETRACKS\""
		fi
	fi

	# Add original MKV file to command
	CMD="$CMD \"$MKVFILE\""

	# If user wants new AC3 as default then add appropriate arguments to command
	if [ $DEFAULT ]; then
		CMD="$CMD --default-track 0"
	fi
	
	# If the language was set for the original DTS track set it for the AC3
	if [ $DTSLANG ]; then
		CMD="$CMD --language 0:$DTSLANG"
	fi

	CMD="$CMD \"$AC3FILE\""

	# Run it!
	$CMD

	if [ $? -ne 0 ]; then
		echo "ERROR: Merging the AC3 track back into the MKV failed."
		
		rm -f "$AC3FILE" #clean up
		rm -f "$NEWFILE" #clean up
		exit
	fi

	# Delete AC3 file
	rm -f "$AC3FILE"
	
	if [ $? -ne 0 ]; then
		echo "WARNING: Could not delete temporary file '$AC3FILE'. Please do this manually after the script has completed."
	fi
fi

# Check to see if the two files are on the same device
NEWFILEDEVICE=$(df "$NEWFILE" | tail -n 1 | cut -d" " -f1)
DSTFILEDEVICE=$(df "$DEST" | tail -n 1 | cut -d" " -f1)

if [ $NEWFILEDEVICE -eq $DSTFILEDEVICE ]; then
	# If we're working on the same device just move the file over the old one
	mv "$NEWFILE" "$MKVFILE"
else
	# Check there is enough free space for the new file
	MKVFILEDIFF=$(($(du "$NEWFILE" | awk '{print $1}') - $MKVFILESIZE))
	DESTFREESPACE=$(df "$DEST" | tail -n 1 | awk '{print $4}')
	if [ $MKVFILEDIFF -gt $DESTFREESPACE ]; then
		echo "ERROR: There is not enough free space to copy the new MKV over the old one. Free up some space and then copy '$NEWFILE' over '$MKVFILE'."
		exit
	fi
	
	# Copy our new MKV with the AC3 over the old one OR if we're using the -e
	# switch then this actually copies the AC3 file to the original directory
	cp "$NEWFILE" "$MKVFILE"
	
	# Check file sizes are equal to ensure the full file was copied
	if [ [ $? -ne 0 ] -o [ $(du "$NEWFILE" | awk '{print $1}') -ne $(du "$MKVFILE" | awk '{print $1}') ] ]; then
		echo "ERROR: There was an error copying the new MKV over the old one. You can perform this manually by copying '$NEWFILE' over '$MKVFILE'."
		exit
	fi
	
	# Remove new file in $WD
	rm -f "$NEWFILE"
	
	if [ $? -ne 0 ]; then
		echo "WARNING: Could not delete temporary file '$NEWFILE'. Please do this manually after the script has completed."
	fi
fi

# Display total execution time
END=$(date +%s)
echo "Total processing time: $(($END - $START)) seconds."