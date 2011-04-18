#!/usr/bin/env python

import sys
if sys.version_info < (2, 3):
    raise RuntimeError('Python 2.3+ is required.')

import logging
import os
import shutil
import subprocess
import unittest

import tests


TEST_FILE_NAME = 'test.mkv'
BASE_PATH = os.path.dirname(__file__)
WORK_PATH = os.path.join(BASE_PATH, 'work')
TEST_FILE = os.path.join(BASE_PATH, TEST_FILE_NAME)


def main():
    if os.path.exists(WORK_PATH):
        shutil.rmtree(WORK_PATH)
    os.mkdir(WORK_PATH)

    if not os.path.exists(TEST_FILE):
        raise ValueError('Could not locate test file.')

    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromModule(tests)
    ]))

    shutil.rmtree(WORK_PATH)
    
if __name__ == '__main__':
    main()


class Base(unittest.TestCase):
    def setUp(self):
        self.work_path = os.path.join(WORK_PATH, self.__class__.__name__)
        self.test_file = os.path.join(self.work_path, TEST_FILE_NAME)

        if os.path.exists(self.work_path):
            raise ValueError('Work path "%s" already exists.' % self.work_path)
        os.mkdir(self.work_path)
        shutil.copyfile(TEST_FILE, self.test_file)

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.test_file))

    def test_file_valid(self):
        output = subprocess.Popen(['mkvmerge', '-i', TEST_FILE_NAME], cwd=self.work_path, stdout=subprocess.PIPE).communicate()[0]
	output = output.replace('\r', '').strip()
        self.assertEquals(output, '''File 'test.mkv': container: Matroska\nTrack ID 1: video (V_MPEG4/ISO/AVC)\nTrack ID 2: audio (A_DTS)\nTrack ID 3: subtitles (S_TEXT/UTF8)\nTrack ID 4: subtitles (S_TEXT/UTF8)''')

    def tearDown(self):
        shutil.rmtree(self.work_path)
