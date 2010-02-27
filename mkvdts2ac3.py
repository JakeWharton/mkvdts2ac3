#!/usr/bin/env python

import os
import re
import sys
from optparse import OptionParser, OptionGroup

version = '''
mkvdts2ac3-2.0.0pre - by Jake Wharton <jakewharton@gmail.com> and
                         Chris Hoekstra <chris.hoekstra@gmail.com>
'''

DEFAULT_ALL = False
DEFAULT_MARK_DEFAULT = False
DEFAULT_KEEP_EXTERNAL = False
DEFAULT_FORCE = False
DEFAULT_KEEP_DTS = False
DEFAULT_NO_DTS = False
DEFAULT_PRIORITY = 0
DEFAULT_WD = '/tmp'
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
parser = OptionParser(usage="Usage: %prog [options] file1 [... fileN]", version=version)

group = OptionGroup(parser, "Configuration Options")
group.add_option('-a', '--all', dest='parse_all', action='store_true', default=DEFAULT_ALL, help='Parse all DTS tracks in MKV.')
group.add_option('-c', '--custom', dest='custom_title', help='Specify custom AC3 track title.')
group.add_option('-d', '--default', dest='mark_default', action='store_true', default=DEFAULT_MARK_DEFAULT, help='Mark AC3 track as default.')
group.add_option('-e', '--external', dest='keep_external', action='store_true', default=DEFAULT_KEEP_EXTERNAL, help='Leave generated AC3 track out of file. Does not modify the original MKV.')
group.add_option('-f', '--force', dest='force_process', action='store_true', default=DEFAULT_FORCE, help='Force processing when existing AC3 track is detected.')
group.add_option('-k', '--keep', dest='keep_dts', action='store_true', default=DEFAULT_KEEP_DTS, help='Retain external DTS track (implies -n).')
group.add_option('-n', '--no-dts', dest='no_dts', action='store_true', default=DEFAULT_NO_DTS, help='Do not retain DTS track.')
group.add_option('-p', dest='priority', default=DEFAULT_PRIORITY, help='Niceness priority.')
group.add_option('-t', '--track', dest='track_id', default=None, help='Specify alternate DTS track ID.')
group.add_option('-w', '--wd', dest='working_dir', default=DEFAULT_WD, help='Specify working directory for temporary files.')
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

options, args = parser.parse_args()


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
	warn('`-a` overrides `-n %s`.', options.track_id)
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
if len(args) == 0:
	error('You must include at least one file.')
	exit = True
if exit: sys.exit(1)


RE_MKVMERGE_INFO = re.compile(r'''Track ID (?P<id>\d+): (?P<type>video|audio|subtitles) \((?P<codec>[A-Z_/]+)\)''')
RE_MKVINFO_AUDIO = re.compile(r'''''')


#Iterate over input files
for arg in args:
	info('Processing "%s"...' % arg)

	#Check if the file exists
	#if not os.path.isfile(arg):
	#	error('Invalid file "%s". Skipping...', arg)
	#	continue
	if not arg.endswith('.mkv'):
		error('File does not appear to be a Matroska file. Skipping...')
		continue

	mkvpath = os.path.dirname(arg)
	mkvfile = os.path.basename(arg)
	mkvname = mkvfile[:-4] # Remove ".mkv"
	debug('mkvpath = %s', mkvpath)
	debug('mkvfile = %s', mkvfile)
	debug('mkvname = %s', mkvname)

	#TODO: get tracks
	tracks = [2,4,5]

	#Iterate over file's DTS tracks
	for track in tracks:
		info('Processing track %s of "%s"...', track, mkvfile)