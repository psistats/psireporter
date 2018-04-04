#!/usr/bin/env python

import os
import shutil

dirs = ['./htmlcov', './dist', './.tox', './.pytest_cache']
files = ['./.coverage', './coverage.xml']

for dirname in dirs:
    if os.path.exists(dirname):
        shutil.rmtree(dirname)

for fn in files:
    if os.path.exists(fn):
        os.remove(fn)

