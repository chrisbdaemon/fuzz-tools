#!/usr/bin/env python3

import re
import csv

with open("out") as f:
    lines = f.readlines()
f = open("summary.csv", "w")
csvwriter = csv.writer(f)

summary_entry = [None, 0, None, None, None]
for line in lines:
    m = re.search(r"Reading.+(\d{4}-\d{2}-\d{2}-\d{2}).info", line)
    if m is not None:
        print(m.groups()[0])
        summary_entry[0] = m.groups()[0]
        continue
    m = re.search(r"lines.+ (\d{1,2}\.\d{1,2})\%", line)
    if m is not None:
        print(m.groups()[0])
        summary_entry[2] = m.groups()[0]
        continue
    m = re.search(r"functions.+ (\d{1,2}\.\d{1,2})\%", line)
    if m is not None:
        print(m.groups()[0])
        summary_entry[3] = m.groups()[0]
    m = re.search(r"branches.+ (\d{1,2}\.\d{1,2})\%", line)
    if m is not None:
        print(m.groups()[0])
        summary_entry[4] = m.groups()[0]
        summary_entry[1] += 1
        csvwriter.writerow(summary_entry)
