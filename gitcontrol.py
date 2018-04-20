#!/usr/bin/env python

import os

indexed_files = [
    'main.py',
    'pix.kv'
]


for file in indexed_files:
    if os.path.exists(file):
        os.system("git add {}".format(file))
