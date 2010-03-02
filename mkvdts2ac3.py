#!/usr/bin/env python

import os
import re
import shutil
import subprocess
import sys
from optparse import OptionParser, OptionGroup

#Script defaults
DEFAULT_ALL = False
DEFAULT_MARK_DEFAULT = False
DEFAULT_KEEP_EXTERNAL = False
DEFAULT_FORCE = False
DEFAULT_INITIAL = False
DEFAULT_KEEP_DTS = False
DEFAULT_LEAVE_NEW = False
DEFAULT_NO_DTS = False
DEFAULT_COPY_NEW = False
DEFAULT_PRIORITY = 0
DEFAULT_WD = '/tmp'

DEFAULT_CUSTOM_AFTEN = []
DEFAULT_CUSTOM_DCADEC = []

DEFAULT_COLOR = True
DEFAULT_QUIET = False
DEFAULT_VERBOSE = False

#Try loading user defaults
try:
    pass
    #TODO: try importing ~/.mkvdts2ac3.defaults.py
except ImportError:
    pass



#Argument parsing
version = '''
mkvdts2ac3-2.0.0pre - by Jake Wharton <jakewharton@gmail.com> and
                         Chris Hoekstra <chris.hoekstra@gmail.com>
'''
parser = OptionParser(usage="Usage: %prog [options] file1 [... fileN]", version=version)

group = OptionGroup(parser, "Configuration Options")
group.add_option('-a', '--all', dest='parse_all', action='store_true', default=DEFAULT_ALL, help='Parse all DTS tracks in MKV.')
group.add_option('-c', '--custom', dest='custom_title', help='Specify custom AC3 track title.')
group.add_option('-d', '--default', dest='mark_default', action='store_true', default=DEFAULT_MARK_DEFAULT, help='Mark AC3 track as default.')
group.add_option('-e', '--external', dest='keep_external', action='store_true', default=DEFAULT_KEEP_EXTERNAL, help='Leave generated AC3 track out of file. Does not modify the original MKV.')
group.add_option('-f', '--force', dest='force_process', action='store_true', default=DEFAULT_FORCE, help='Force processing when existing AC3 track is detected.')
group.add_option('-i', '--initial', dest='is_initial', action='store_true', default=DEFAULT_INITIAL, help='New AC3 track will be first in file.')
group.add_option('-k', '--keep', dest='keep_dts', action='store_true', default=DEFAULT_KEEP_DTS, help='Retain external DTS track (implies -n).')
group.add_option('-l', '--leave', dest='leave_new', action='store_true', default=DEFAULT_LEAVE_NEW, help='Leave new MKV in working directory.')
group.add_option('-n', '--no-dts', dest='no_dts', action='store_true', default=DEFAULT_NO_DTS, help='Do not retain DTS track.')
group.add_option('--new', dest='copy_new', action='store_true', default=DEFAULT_COPY_NEW, help='Do not copy over original. Create new adjacent file.')
group.add_option('-p', dest='priority', default=DEFAULT_PRIORITY, help='Niceness priority.')
group.add_option('-t', '--track', dest='track_id', default=None, help='Specify alternate DTS track ID.')
group.add_option('-w', '--wd', dest='working_dir', default=DEFAULT_WD, help='Specify working directory for temporary files.')
parser.add_option_group(group)

group = OptionGroup(parser, 'Subprocess Options')
group.add_option('-A', dest='custom_aften', action='append', default=DEFAULT_CUSTOM_AFTEN, help='Pass custom arguments to aften.')
group.add_option('-D', dest='custom_dcadec', action='append', default=DEFAULT_CUSTOM_DCADEC, help='Pass custom arguments to dcadec.')
parser.add_option_group(group)

group = OptionGroup(parser, "Testing Options")
group.add_option('--test', dest='is_test', action='store_true', default=False, help='Print commands only, execute nothing.')
group.add_option('--debug', dest='is_debug', action='store_true', default=False, help='Print commands and pause before executing each.')
parser.add_option_group(group)

group = OptionGroup(parser, "Display Options")
group.add_option('-m', '--no-color', dest='is_color', action='store_false', default=DEFAULT_COLOR, help='Do not use colors (monochrome).')
group.add_option('-q', '--quiet', dest='is_quiet', action='store_true', default=DEFAULT_QUIET, help='Output nothing to the terminal.')
group.add_option('-v', '--verbose', dest='is_verbose', action='store_true', default=DEFAULT_VERBOSE, help='Turn on verbose output.')
parser.add_option_group(group)

options, mkvfiles = parser.parse_args()

#Script header
if not options.is_quiet:
    parser.print_version()



#Color functions
red    = lambda text: ('\033[1;31m%s\033[0m' % text) if options.is_color else text
green  = lambda text: ('\033[1;32m%s\033[0m' % text) if options.is_color else text
blue   = lambda text: ('\033[1;34m%s\033[0m' % text) if options.is_color else text
yellow = lambda text: ('\033[1;33m%s\033[0m' % text) if options.is_color else text

def debug(text, *args):
    if options.is_verbose:
        print yellow('DEBUG: ') + text % args
def info(text, *args):
    if not options.is_quiet:
        print blue('INFO: ') + text % args
def warn(text, *args):
    if not options.is_quiet:
        print red('WARNING: ') + text % args
def error(text, *args):
    if not options.is_quiet:
        print red('ERROR: ') + text % args



#Check argument restrictions
exit = False
if options.keep_dts:
    options.no_dts = True
if options.no_dts and options.keep_external:
    error('Options `-e` and `-n` are mutually exclusive.')
    exit = True
if options.track_id and options.parse_all:
    warn('`-n %s` overrides `-a`.', options.track_id)
if options.is_quiet and options.is_verbose:
    error('Options `-q` and `-v` are mutually exclusive.')
    exit = True
if options.is_test and options.is_debug:
    error('Options `--test` and `--debug` are mutually exclusive.')
    exit = True
if options.mark_default and options.keep_external:
    warn('`-e` overrides `-d`.')
if options.custom_title and options.keep_external:
    warn('`-c` is not needed with `-d`.')
if len(mkvfiles) == 0:
    error('You must include at least one file.')
    exit = True
if exit: sys.exit(1)


RE_MKVMERGE_INFO = re.compile(r'''Track ID (?P<id>\d+): (?P<type>video|audio|subtitles) \((?P<codec>[A-Z0-9_/]+)\)''')
DTS_FILE = '%s.%s.dts'
AC3_FILE = '%s.%s.ac3'
TC_FILE  = '%s.%s.tc'
NEW_FILE = '%s.new.mkv'


#Iterate over input files
for mkvfile in mkvfiles:
    info('Processing "%s"...' % mkvfile)

    #Check if the file exists
    if not os.path.isfile(mkvfile):
        error('Invalid file "%s". Skipping...', mkvfile)
        continue
    if not mkvfile.endswith('.mkv'):
        error('File does not appear to be a Matroska file. Skipping...')
        continue


    mkvpath  = os.path.dirname(mkvfile)
    mkvname  = os.path.basename(mkvfile)
    mkvtitle = mkvname[:-4] #Remove ".mkv" extension
    debug('mkvpath  = %s', mkvpath)
    debug('mkvname  = %s', mkvname)
    debug('mkvtitle = %s', mkvtitle)


    #Get mkvmerge info and mkvinfo for the tracks
    mkvtracks = {}
    mkvmergeinfo = subprocess.Popen(['mkvmerge', '-i', mkvfile], stdout=subprocess.PIPE).communicate()[0]
    mkvinfo = subprocess.Popen(['mkvinfo', mkvfile], stdout=subprocess.PIPE).communicate()[0]
    for match in RE_MKVMERGE_INFO.finditer(mkvmergeinfo):
        matchdict = match.groupdict()
        id = matchdict.pop('id')
        debug('Found track %s: %s.', id, matchdict)
        mkvtracks[id] = matchdict

        #TODO: parse mkvinfo
        mkvtracks[id]['dts_lang'] = 'und'
        mkvtracks[id]['dts_name'] = None


    #Get DTS tracks which need parsing
    parsetracks = {}
    if options.track_id is not None:
        if track_id not in mkvtracks.keys():
            error('Explicitly defined track id does not exist in file.')
            continue
        if mkvtracks[options.track_id]['codec'] != 'A_DTS':
            error('Explicitly defined track id is not a DTS track.')
            continue
        parsetracks[options.track_id] = mkvtracks[options.track_id]
        debug('Using argument specified track id %s.', options.track_id)
    elif options.parse_all:
        parsetracks = dict((id, info) for id, info in mkvtracks.iteritems() if info['codec'] == 'A_DTS')
        if len(parsetracks) == 0:
            error('No DTS tracks found in file.')
            continue
        debug('Using track %s %s.', 'id' if len(parsetracks) == 1 else 'ids', ', '.join(parsetracks.keys()))
    else:
        tracks = [id for id in mkvtracks.keys() if mkvtracks[id]['codec'] == 'A_DTS']
        if len(tracks) == 0:
            error('No DTS tracks found in file.')
            continue
        parsetracks[tracks[0]] = mkvtracks[tracks[0]]
        debug('Using track id %s.', tracks[0])


    #Extract timecodes for the tracks
    info('Extracting timecodes...')
    cmd = ['mkvextract', 'timecodes_v2', mkvfile]
    for track in parsetracks.keys():
        tc_file = parsetracks[track]['tc_file'] = os.path.join(options.working_dir, TC_FILE % (mkvtitle, track))
        cmd.append('%s:%s' % (track, tc_file))
        debug('Track %s to "%s".', track, tc_file)
    if not options.is_test:
        subprocess.Popen(cmd).wait()

    #Parse timecodes for each track
    for track in parsetracks.keys():
        if not options.is_test:
            f = open(parsetracks[track]['tc_file'])
            f.readline()
            delay = f.readline().strip()
            f.close()
        else:
            delay = 0

        parsetracks[track]['dts_delay'] = delay
        debug('Track %s delay = %sms.' % (track, delay))

    #Extract DTS tracks
    info('Extracting DTS tracks...')
    cmd = ['mkvextract', 'tracks', mkvfile]
    for track in parsetracks.keys():
        dts_file = parsetracks[track]['dts_file'] = os.path.join(options.working_dir, DTS_FILE % (mkvtitle, track))
        cmd.append('%s:%s' % (track, dts_file))
        debug('Track %s to "%s".', track, dts_file)
    if not options.is_test:
        subprocess.Popen(cmd).wait()

    #Convert DTS to AC3
    info('Converting DTS to AC3...')
    for track in parsetracks.keys():
        ac3_file = parsetracks[track]['ac3_file'] = os.path.join(options.working_dir, AC3_FILE % (mkvtitle, track))
        debug('Track %s to "%s".', track, ac3_file)

        #Assemble dcadec command
        dcadec = ['dcadec']
        pairs = {'-o': 'wavall'}
        for pair in options.custom_dcadec:
            arg, value = pair.split('=', 1)
            pairs[arg] = value
            debug('Custom dcadec args: %s %s.' % (arg, value))
        for arg, value in pairs.iteritems():
            dcadec.append(arg)
            dcadec.append(value)
        dcadec.append(parsetracks[track]['dts_file'])

        #Assemble aften command
        aften = ['aften']
        for pair in options.custom_aften:
            arg, value = pair.split('=', 1)
            aften.append(arg)
            aften.append(value)
            debug('Custom aften args: %s %s.' % (arg, value))
        aften.append('-')
        aften.append(parsetracks[track]['ac3_file'])

        #Do the conversion
        if not options.is_test:
            dcadec_cmd = subprocess.Popen(dcadec, stdout=subprocess.PIPE)
            aften_cmd  = subprocess.Popen(aften, stdin=dcadec_cmd.stdout).wait()

            #Get DTS and AC3 file sizes
            parsetracks[track]['dts_size'] = os.path.getsize(parsetracks[track]['dts_file'])
            parsetracks[track]['ac3_size'] = os.path.getsize(ac3_file)

            #Delete DTS files
            if not options.keep_dts:
                os.remove(parsetracks[track]['dts_file'])

    if options.keep_external:
        info('Copying AC3 files to MKV directory...')
        for track, trackinfo in parsetracks.iteritems():
            debug('Track %s from "%s" to "%s".', track, trackinfo['ac3_file'], mkvpath)
            if not options.is_test:
                shutil.copy2(trackinfo['ac3_file'], mkvpath)
    else:
        cmd = ['mkvmerge', '-q']

        if options.is_initial:
            #Put AC3 track(s) first in the file
            cmd.append('--track-order')
            order = ['0:1']
            for i in range(len(parsetracks)):
                i += 1
                order.append('%s:0' % i)
            cmd.append(','.join(order))

        #Declare output file
        cmd.append('-o')
        cmd.append(NEW_FILE % mkvtitle)

        if options.no_dts:
            #Find non-DTS tracks (if any) to save
            save_tracks = [track for track, trackinfo in mkvtracks if track not in parsetracks.keys() and trackinfo['codec'].startswith('A_')]
            if save_tracks:
                cmd.append('-a')
                cmd.append(','.join(save_tracks))
            else:
                cmd.append('-A')

        #Add original MKV file
        cmd.append(mkvfile)

        for track, trackinfo in parsetracks.iteritems():
            if options.mark_default:
                #Mark first new AC3 track as default
                cmd.append('--default-track')
                cmd.append(0)
                options.mark_default = False #So this only fires once

            #Copy over the languages from respective DTS tracks
            cmd.append('--language')
            cmd.append('0:%s' % trackinfo['dts_lang'])

            #Add delay if there was one on the original DTS
            delay = int(trackinfo['dts_delay'])
            if delay > 0:
                cmd.append('--sync')
                cmd.append('0:%s' % delay)

            #Copy the track name if one existed on the DTS
            if trackinfo['dts_name']:
                cmd.append('--track-name')
                cmd.append('0:"%s"' % trackinfo['dts_name'])

            #Append this AC3 file
            cmd.append(trackinfo['ac3_file'])

        #Run main remux
        debug('Main command: ' + ' '.join(cmd))
        if not options.is_test:
            subprocess.Popen(cmd).wait()

        #Delete AC3 files
        for track in parsetracks.keys():
            debug('Deleting "%s"...', parsetracks[track]['ac3_file'])
            if not options.is_test:
                os.remove(parsetracks[track]['ac3_file'])