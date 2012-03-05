`mkvdts2ac3` is a bash script which can be used for converting the DTS in
Matroska (MKV) files to AC3. It provides you with a healthy set of options
for controlling the resulting file.

Installation
============

Prerequisites
-------------
Make sure the executables for the following libraries are accessible.

1. [mkvtoolnix](http://www.bunkus.org/videotools/mkvtoolnix/) - Matroska tools
2. [ffmpeg](http://ffmpeg.org/) - Audio conversion tool
3. [rsync](http://rsync.samba.org/) - File transfer and synchronization

*Note: If you are a Mac OS X user you may need to compile these libraries.*

Installation
------------
If you have `git` installed, you can just run
`git clone git://github.com/JakeWharton/mkvdts2ac3.git`.

You can download the script directly with wget or curl:
  wget https://raw.github.com/JakeWharton/mkvdts2ac3/master/mkvdts2ac3.sh
  -or-
  curl -O https://raw.github.com/JakeWharton/mkvdts2ac3/master/mkvdts2ac3.sh

Otherwise you can click the "Download" link on the GitHub project page and
download an archive and extract its contents.

Optional: If you want easy access to the script from any directory you can copy
or symlink the `mkvdts2ac3.sh` file to a directory in your PATH variable or else
append the script's directory to the PATH variable.

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

    mkvdts2ac3-1.5.3 - by Jake Wharton <jakewharton@gmail.com> and
                          Chris Hoekstra <chris.hoekstra@gmail.com>

    Usage: mkvdts2ac3.sh [options] <filename>
    Options:
         -c TITLE,        Custom AC3 track title.
         --custom TITLE
         -d, --default    Mark AC3 track as default.
         -e, --external   Leave AC3 track out of file. Does not modify the
                          original matroska file. This overrides '-n' and
                          '-d' arguments.
         -f, --force      Force processing when AC3 track is detected
         -i, --initial    New AC3 track will be first in the file.
         -k, --keep-dts   Keep external DTS track (implies '-n').
         -m, --nocolor    Do not use colors (monotone).
         --md5            Perform MD5 comparison when copying across drives.
         -n, --no-dts     Do not retain the DTS track.
         --new            Do not copy over original. Create new adjacent file.
         -p PRIORITY      Modify niceness of executed commands.
         -s MODE,
         --compress MODE  Apply header compression to streams (See mkvmerge's --compression).
         -t TRACKID,
         --track TRACKID  Specify alternate DTS track.
         -w FOLDER,
         --wd FOLDER      Specify alternate temporary working directory.

         --test           Print commands only, execute nothing.
         --debug          Print commands and pause before executing each.

         -h, --help       Print command usage.
         -v, --verbose    Turn on verbose output
         -V, --version    Print script version information.


User Defaults
-------------
If you find yourself constantly using the same settings, you can create a
configuration file to automatically set them. Copy the following to
`~/.mkvdts2ac3.rc` and uncomment whichever lines you wish.

    #EXTERNAL=1
    #NODTS=1
    #KEEPDTS=1
    #DEFAULT=1
    #FORCE=1
    #INITIAL=1
    #NOCOLOR=1
    #MD5=1
    #NEW=1
    #PRIORITY=0
    #DTSTRACK=
    #DTSNAME=
    #COMP="none"

*(Note: If `EXTERNAL` is set then `NODTS` and `KEEPDTS` should not be used.
`AUDIOMODE` is the `-o`-flag value passed to `aften`. `PRIORITY` is the
niceness value. `DTSNAME` is custom title for new AC3 track.)*


Examples
--------
Keep only the new AC3 track, discarding the original DTS

    mkvdts2ac3.sh -n Some.Random.Movie.mkv

Specify an alternate directory to use for the temporary files. This can be
useful when the partition your `/tmp` directory on is tiny.

    mkvdts2ac3.sh -w /mnt/bigHDD Some.Random.Movie.mkv

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

    mkvdts2ac3.sh -d -t 3 -w /mnt/media/tmp/ Some.Random.Movie.mkv

If you're unsure of what any command will do run it with the `--test` argument
to display a list of command execute. You can also use the `--debug` argument
which will print out the commands and wait for the user to press the return key
before running each.

    $ ./mkvdts2ac3.sh --test -d -t 3 -w /mnt/media/tmp Some.Random.Movie.mkv
    
    mkvdts2ac3-1.5.3 - by Jake Wharton <jakewharton@gmail.com> and
                          Chris Hoekstra <chris.hoekstra@gmail.com>
    
    MKV FILE: Some.Random.Move.mkv
    DTS FILE: /mnt/media/tmp/Some.Random.Movie.dts
    AC3 FILE: /mnt/media/tmp/Some.Random.Movie.ac3
    TIMECODE: /mnt/media/tmp/Some.Random.Movie.tc
    NEW FILE: /mnt/media/tmp/Some.Random.Movie.new.mkv
    WORKING DIRECTORY: /mnt/media/tmp
    Checking to see if DTS track specified via arguments is valid.
    > mkvmerge -i "Some.Random.Movie.mkv" | grep "Track ID 3: audio (A_DTS)"
    
    Extract track information for selected DTS track.
    > mkvinfo "Some.Random.Movie.mkv" | grep -A 25 "Track number: 3"
    
    Extract language from track info.
    > echo "INFO" | grep -m 1 "Language" | cut -d " " -f 5
    
    Extract name for selected DTS track. Change DTS to AC3 and update bitrate if present.
    > echo "INFO" | grep -m 1 "Name" | cut -d " " -f 5- | sed "s/DTS/AC3/" | awk '{gsub(/[0-9]+(\.[0-9]+)?(M|K)bps/,"448Kbps")}1'
    
    Extract timecode information for the audio track.
    > mkvextract timecodes_v2 "Some.Random.Movie.mkv" 3:"/mnt/media/tmp/Some.Random.Movie.tc"
    > sed -n "2p" "/mnt/media/tmp/Some.Random.Movie.tc"
    > rm -f "/mnt/media/tmp/Some.Random.Movie.tc"
    
    Extract DTS file from MKV.
    > mkvextract tracks "Some.Random.Movie.mkv" 3:"/mnt/media/tmp/Some.Random.Movie.dts"
    Converting DTS to AC3.
    > ffmpeg -i "/mnt/media/tmp/Some.Random.Movie.dts" -acodec ac3 -ac 6 -ab 448k "/mnt/media/tmp/Some.Random.Movie.ac3"
    
    Running main remux.
    > nice -n 0 mkvmerge -q -o "/mnt/media/tmp/Some.Random.Movie.new.mkv" --compression 1:none "Some.Random.Movie.mkv" --default-track 0 --language     0:DTSLANG --track-name 0:"DTSNAME" --sync 0:DELAY --compression 0:none "/mnt/media/tmp/Some.Random.Movie.ac3"
    Removing temporary AC3 file.
    > rm -f "/mnt/media/tmp/Some.Random.Movie.ac3"
    
    Copying new file over the old one.
    > cp "/mnt/media/tmp/Some.Random.Movie.new.mkv" "Some.Random.Movie.mkv"
    
    Remove working file.
    > rm -f "/mnt/media/tmp/Some.Random.Movie.new.mkv"


Developed By
============
* Jake Wharton - <jakewharton@gmail.com>
* Chris Hoekstra - <chris.hoekstra@gmail.com>

Git repository located at
[github.com/JakeWharton/mkvdts2ac3](http://github.com/JakeWharton/mkvdts2ac3)


Very Special Thanks
-------------------
* Philipp Winkler - Munich, Germany
* Paul Tilley
* Paulo Ferreira
* Douglas Carter

Thanks
------
The following people contributed useful thoughts or code to `mkvdts2ac3`:

* John Nilsson - Dependency, file, and space checking as well as general bash formatting.
* crimsdings - General debugging and error resolution.
* Vladimir Berezhnoy - Feature to copy track name from DTS.
* Ricardo Capurro - Bug reporting on uncommon uses.
* Tom Flanagan - Idea for downmixing support.
* lgringo - Suggestion to copy audio track delay.
* Huss - Suggestion of ability to set niceness.
* Florian Beverborg - Suggestion of `--new` argument to leave original untouched.
* Daniele Nicolucci - `df` portability fixes.
* Florian Coulmier - Bug reports and patches.
* NameLessJedi - Header compression disabling suggestion.
* d4nyl0 - Transition to ffmpeg
* n-i-x - Progress display on file copy

And to everyone who submitted bug reports through email and on networkedmediatank.com!


License
=======

    Copyright 2011 Jake Wharton

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
