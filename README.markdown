mkvdts2ac3
===========
`mkvdts2ac3` is a bash script which can be used for converting the DTS in
Matroska (MKV) files to AC3. It provides you with a healthy set of options
for controlling the resulting file.

Installation
============

Prerequisites
-------------
Make sure the executables for the following libraries are accessible.

1.  mkvtoolnix - Matroska tools  
    http://www.bunkus.org/videotools/mkvtoolnix/

2.  libdca - DTS to WAV decoder      
    http://videolan.org/developers/libdca.html

3.  aften - WAV to AC3 encoder  
    http://aften.sourceforge.net/

Installation
------------
1.  If you have `git` installed, you can just run
    `git://github.com/JakeWharton/mkvdts2ac3.git`. Otherwise you can click
    the "Download" link on the GitHub project page and download an archive
    and extract its contents.

2.  `cd` into the directory and you need to set the main script as executable
    by running the following command:
        chmod +x mkvdts2ac3.sh

3.  *(Optional)* If you want easy access to the script from any directory you
    can copy the `mkvdts2ac3.sh` file to a directory in your PATH or else
    append the script's directory to the PATH.

Usage
=====
This script was designed to be very simple and will automatically convert the
first DTS track it finds in a Matroska file to AC3 and append it when run
without any arguments. Since this was the most common scenario for the
developer it is the default action.
    mkvdts2ac3.sh Some.Random.Movie.mkv

For users who wish to change the behavior there are a variety of options which
control various aspects of the script. Here is the output of the `--help`
argument.
    mkvdts2ac3-1.0.0b - by Jake Wharton <jakewharton@gmail.com>
    
    Usage: ./mkvdts2ac3.sh [options] <filename>
    Options:
         -h, --help       Print command usage
         -v, --version    Print script version information
    
         -d, --default    Mark AC3 track as default
         -e, --external   Leave AC3 track out of file. Does not modify the
                          original matroska file. This overrides '-n' and
                          '-d' arguments.
         -k, --keep-dts   Keep external DTS track (implies '-n')
         -n, --no-dts     Do not retain the DTS track
         -t TRACKID,
         --track TRACKID  Specify alternate DTS track
         -w FOLDER,
         --wd FOLDER      Specify alternate temporary working directory
    
         --test           Print commands only, execute nothing.
         --debug          Print commands and pause before executing each.

Examples
--------
Keep only the new AC3 track, discarding the original DTS
    mkvdts2ac3.sh -n Some.Random.Movie.mkv

Specify an alternate directory to use for the temporary files. This can be
useful when the partition your `/tmp` directory on is tiny.
    mkvdts2ac3.sh -WD /mnt/bigHDD Some.Random.Movie.mkv

Convert a different DTS track rather than the first one sequentially in the
file. This will require you to check the output of a command like
`mkvmerge -i Some.Random.Movie.mkv` which will give you the track ids of each
file.
    mkvdts2ac3.sh -t 4 Some.Random.Movie.mkv

If you want to retain the DTS track in an alternate location you can instruct
the script not to delete it after the conversion.
    mkvdts2ac3.sh -k Some.Random.Movie.mkv

If you want to keep the original file untouched (such as if you are still
seeding it in a torrent) and your player supports external audio tracks you
can choose to leave the converted AC3 track out of the file.
    mkvdts2ac3.sh -e Some.Random.Movie.mkv

All of these examples only showcase the use of a single argument but they can
be combined to achieve the desired result.
    mkvdts2ac3.sh -d -t 3 -WD /mnt/media/tmp/ Some.Random.Movie.mkv

Developed By
============
* Jake Wharton - <jakewharton@gmail.com>

Git repository located at
[github.com/JakeWharton/mkvdts2ac3](http://github.com/JakeWharton/mkvdts2ac3)


License
=======
    Copyright 2009 Jake Wharton
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
       http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.