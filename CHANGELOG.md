Change Log
==========

Version 1.6.0 *(2012-01-26)*
----------------------------

New Features:

 * Script now uses `ffmpeg` instead of `libdca`/`aften` for better conversion.

Bug Fixes:

 * Ensure proper audio output mode is displayed when logging verbosely.
 * Display progress of file copy to make it clear that the script is still doing work.

*thanks to GitHub user n-i-x for the progress patch*


Version 1.5.7 *(2011-10-06)*
----------------------------

Bug Fixes:

 * Make parsing rules of audio track info from `mkvinfo` much more strict to we ensure only our desired track info is retrieved.

*thanks to GitHub user mihaic for this fix*


Version 1.5.6 *(2011-10-03)*
----------------------------

Bug Fixes:

 * Properly fix aforementioned logic flaw to use integer testing to restore `--keep-dts` to proper operation.


Version 1.5.5 *(2011-08-19)*
----------------------------
Bug Fixes:

* Fix minor logic flaw when `--keep-dts` was used that harmlessly printed a warning.
* Properly format info, warning, and error messages.

*thanks to Ademar de Souza Reis Jr for these fixes*


Version 1.5.4 *(2011-08-03)*
----------------------------
Bug Fixes:

* Proper checking of `--keep-dts` flag.
* Fix `.deb` building for all platforms.
* Ensure locale is set to English for `mkvinfo` parsing.


Version 1.5.3 *(2011-04-22)*
----------------------------
Bug Fixes:

* Fix KB to B comparison on free space check.
* Force POSIX output on all platforms to ensure the correct column is always being referenced.
* Ensure MD5s are being properly compared when requested (thanks Florian Coulmier).
* Copy DTS file to the same folder as MKV when `-k`/`--keep` flag is set.
* Force skip the use of any MKV header compression to ensure the most compatible file.


Version 1.5.2 *(2010-08-24)*
----------------------------
New Features:

* User-loadable defaults can now be stored in the `~/.mkvdts2ac3.rc` file. See the README for file specification.

Bug Fixes:

* Use portable size check for `df` (thanks Daniele Nicolucci).


Version 1.5.1 *(2010-02-15)*
----------------------------
New Features:

* `-i`/`--initial` argument which places the AC3 track as the first audio track in the file.
* `--new` argument does not overwrite the original file but instead creates a new one with `-AC3` appended to the file name.
* Remove `du` usage in favor of optional MD5 comparison which is more reliable cross-filesystem and cross-platform.

Bug Fixes:

* Refactor cleanup command so the external AC3 and keep DTS command work properly.
* Don't attempt a same device move if the new and destination file are the same. This can occur if you are keeping the AC3 external and using a working directory that is the same as the location of the movie file.


Version 1.5.0 *(2009-12-08)*
----------------------------
New Features:

* Merged Jake Wharton's 1.0.6-2-JDW with Chris Hoekstra's 1.0.6.3-CCH massive upgrades


Version 1.0.6.3-CCH *(2009-12-08)*
----------------------------------
New Features:

* Moved du/stat cmd to global variable up top for ease of changing

Bug Fixes:

* In certain cases temp files were not getting deleted.  Fixed by doing one cleanup at end and on any exits
* `stat -c` doesn't work on Mac OS/X or BSD systems.  Argh!  Back to `du` and damned be Reiserfs people.

Cleanup:

* Cleaned up the final filesize summary, used printf for alignment and misc tweaks

Known Bugs:

* `-e` doesn't work and didn't [ever?] work as of 1.0.5.  Not sure the intent as it is "do nothing at all" NEEDED?


Version 1.0.6-2-JDW *(2009-12-06)*
----------------------------------
New Features:

* Force the use of 1K byte blocks for filesize and free space comparison EVERYWHERE. By standardizing we (hopefully) eliminate any inconsistencies between different filesystems and (hopefully) have a portable solution.


Version 1.0.6.2-CCH *(2009-12-06)*
----------------------------------
New Features:

* Merged in Jake's 1.0.6-1 changes and updated version number accordingly.
* Created final filesize summary at the end.


Version 1.0.6-1-JDW *(2009-12-05)*
----------------------------------
New Features:

* Ensure `df` and `stat` are both using bytes for comparisons.


Version 1.0.6.1-CCH *(2009-12-05)*
----------------------------------
New Features:

* Merged in Jake's 1.0.6 changes and updated version number accordingly.
* Added a `-m` or `--nocolor` option (monotone) to turn off color highlighting manually.

Cleanup:

* Brought `colors.sh` function `color()` inhouse to remove dependency on my personal external scripts.
* Removed all but used colors, bell and off in `colors()` function


Version 1.0.6-JDW *(2009-12-04)*
--------------------------------
New Features:

* Change `sed` to `awk` for bitrate replacement for a portable solution.
* Change `du` to `stat` for accurate, cross-filesystem byte counts.
* Check for existing AC3 track and exit if present.
* Add `-f`/`--force` argument to ignore any existing AC3s.

Cleanup:

* Hide `aften` output for a nicer display during the transcoding process.


Version 1.0.5.2-CCH *(2009-12-04)*
----------------------------------
Bug Fixes:

* Switched to using `stat` instead of `du` (thanks ctalbot for pointing this out).
* Fixed minor bug of B vs KB comparison with Working Directory (`$WD`).
* Removed contrary logic in `rm $NEWFILE` section.
* Return code for `rsync` was checked after after `du`/`stat` tests. This would never work so 2 seperate tests now.

New Features:

* Added `-f`,`--force` option to force a continuation.  This just appends a redundant AC3 track.
* Changed all `exit` statements to be eiter 0 or 1 depending on exit due to failure or normal exit.
* Added Working Directory (`$WD`) to the default value section per ctalbot request.
* Added returncode check for `mv`/`rsync` copies (Satisfied a Jake TODO).
* Created `cleanup()` function to test and remove files with error code checking inherent.  TODO: ensure every exit scenario.
* Added cleanup routines to checkerror routine when exiting.

Optimizes:

* Converted individual timestamp displays into single line statement and a `timestamp()` function.
* Rearranged functions and variable declarations to improve code readability and maintainability.
* Converted all tool/app dependency checks to single line statements and a `checkdep()` function.
* Compressed multi-page case statement even more by moving comments up a line to save a line per option.
* Implemented a `checkerror()` returncode function .
* Replaced all `rm -f` commands with cleanup and errorcheck routines.
* Added `doprint()` function to handle verbose (`-v`, `--debug`, or `--test`) printing option.
* Replaced all repetitive checks for `$PRINT` with `doprint()` function call.

Cleanup:

* Changed `timestamp()` variables to be more descriptive.
* Removed extraneous spaces scattered throughout case statement and conformed to one standard.
* After 765 lines of `diff` and ~1000 bytes longer we are quite a bit cleaner and easier to follow (IMO).


Version 1.0.5.1-CCH *(2009-12-13)*
----------------------------------
New Features:

* Switched from `cp` and `mv` to `rsync` for better performance.  `rsync` performance speedup is ~20% on my system.
* Added check to see if AC3 track already exists in file so we don't duplicate each time (TODO would be to add a `-f` force).
* Cleaned up output to be much less messy and spamming in general.
* Focused on quieted (`dcadec`/`aften`) output...sssh, stop spamming us.
* Added Major task announcements such as (Extracting DTS Track).
* Added test for `rsync` to ensure it exists on system (ala `mkvmerge`, `dcadec`, etc.).
* Color highlighting to add readability.
* First stages of function optimization for repetitive tasks.
* Granular timestamping for each stage instead of just 1 final time.
* Bell and red highlighting for all errors (error function as well).
* Changed `-v` from version to `--verbose`.  `-V` is now version. (Previously there was no verbose unless debugging or testing).
* Modified help output to reflect new `-v` option and added `-V` option.


Version 1.0.5-JDW *(2009-11-05)*
--------------------------------
New Features:

* Added `-p` argument which will set the "niceness" level of all executed programs.
* If present in track name, 'DTS' will be changed to 'AC3' and the bitrate updated accordingly.
* Delay on the DTS track is now copied over to the new AC3 track.


Version 1.0.4-JDW *(2009-08-28)*
--------------------------------
Bug Fixes:

* Reverted to using non-regex language lookup for portability.


Version 1.0.3-JDW *(2009-07-26)*
--------------------------------
New Features:

* Added support to pass an audio mode through to `dcadec` to allow downmixing (Idea by Tom Flanagan).
* `-c` argument added to allow specifying a custom title for the AC3 track.

Bug Fixes:

* Commonly aliased commands are now escaped with a backslash to ensure proper execution.


Version 1.0.2-JDW *(2009-05-12)*
--------------------------------
New Features:

* Modified script permissions to make it executable "out of the box".

Optimizations:

* `mkvinfo` parsing is now only done once and all values are extracted from result.


Version 1.0.1-JDW *(2009-05-10)*
--------------------------------
New Features:

* Copy DTS track name title over to new AC3 track (thanks to Vladimir Berezhnoy).


Version 1.0.0-JDW *(2009-05-07)*
--------------------------------
Intial Release!
