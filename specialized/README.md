Information
===========

These file are the ones that I personally use to change the audio in my matroska files. Since they are small and specialized they are a lot easier to maintain than the full mkvdts2ac3.sh script.

All of these scripts take only one argument, the matroska file path.

Usage
=====

*   specialized/mkvdts2ac3.sh
    
    1. Extract DTS from MKV
    2. Convert DTS to AC3
    3. Insert AC3 into MKV retaining DTS
    
    This is the barebones version of the mkvdts2ac3.sh script. It will 
perform exactly the same as the main script without any of the optional 
arguments.

*   specialized/mkvdtsextract.sh
    
    1. Extract DTS from MKV
    2. Remux MKV to remove extracted DTS track
    
    This script is useful to pull out DTS tracks after you have 
previously run mkvdts2ac3. I use this to pull out redundant DTS tracks 
and upload them to a seperate place.

*   specialized/mkvdts2ac3_newac3only.sh
    
    1. Extract DTS from MKV
    2. Convert DTS to AC3
    3. Insert AC3 into MKV removing **all other audio tracks**
    
    This script will replace the DTS track with the new AC3 track as 
well as remove any other audio tracks. This is useful when you have 
commentary or alternate language tracks you want to eliminate as well.

*   specialized/mkvdts2ac3_extractdts_keepac3only.sh
    
    1. Extract DTS from MKV
    2. Convert DTS to AC3 but keep DTS file
    3. Insert AC3 into MKV removing **all other audio tracks**
    
    This is the version that I use the most. It converts the DTS track 
to AC3 and removes all other audio tracks in the process. It also leaves 
the extracted DTS in tact so you can store it somewhere else for muxing 
back in at a later time.

*   specialized/mkvdts2ac3_extractdts_addac3.sh
    
    1. Extract DTS from MKV
    2. Convert DTS to AC3 but keep DTS file
    3. Insert AC3 into MKV replacing DTS track
    
    This will perform the same operation as the version above except it 
will only remove the DTS track it converted leaving all the other audio 
tracks (if there are any) intact.
