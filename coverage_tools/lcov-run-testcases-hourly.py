#!/usr/bin/env python

import os
import subprocess
from datetime import datetime


def create_filename(timestamp):
    t = datetime.fromtimestamp(timestamp)
    return "%04d-%02d-%02d-%02d.info" % (t.year, t.month, t.day, t.hour)

files = []
path = "/home/chris/NIST/imagemagick/coverage/testcases/vanilla"
for filename in os.listdir(path):
    filename = path + "/" + filename
    if not os.path.isfile(filename):
        continue

    files.append((filename, os.stat(filename).st_mtime))
sorted_files = sorted(files, key=lambda f: f[1])

total_hours = 0
last_increment = sorted_files[0][1]
for fileinfo in sorted_files:
    timediff = fileinfo[1] - last_increment

    # Create tracefile for every hour
    while timediff >= 3600:
        # initial testcases can have days between timestamps
        if timediff >= 3600*2 and total_hours <= 1:
            last_increment = fileinfo[1]
        else:
            total_hours += 1
            info_filename = create_filename(last_increment)
            cmd_str = "lcov -c -b . -d . --rc lcov_branch_coverage=1 -o %s" % info_filename
            subprocess.call(cmd_str.split())
            last_increment += 3600
        timediff = fileinfo[1] - last_increment
    subprocess.call(["timeout", "5", "./utilities/convert", fileinfo[0], "jpeg:/dev/null"])
