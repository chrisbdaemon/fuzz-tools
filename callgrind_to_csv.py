#!/usr/bin/env python3.5

import subprocess
import re
import os
import ipdb

class Fingerprint:
    exec_file = "/usr/bin/callgrind_annotate"
    
    def __init__(self, filename):
        self.functions = {}
        self.filename = ""
        p = subprocess.Popen([self.exec_file, filename],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode("ascii")

        fmatches = re.search(r"target: .*\/([^\/]+\.pcap)", out, re.MULTILINE)
        if fmatches:
            self.filename = fmatches.groups(0)[0]
        else:
            return None

        lines = out.split("\n")
        for line in lines:
            m = re.search('^\s*([\d,]+) .*:(\S+).*$', line)
            if m:
                match = m.groups(1)
                count = match[0]
                count = int(count.replace(",", ""))
                self.functions[match[1]] = count
                
    def compare_to(self, otherFingerprint):
        diffs = {}

        if len(self.functions) == 0:
            return 1.0
        
        for function in self.functions:
            if function in otherFingerprint.functions:
                if self.functions[function] > otherFingerprint.functions[function]:
                    high = self.functions[function]
                    low = otherFingerprint.functions[function]
                else:
                    high = otherFingerprint.functions[function]
                    low = self.functions[function]
                diffs[function] = 1. - float(low)/float(high)
            else:
                diffs[function] = 1.

        for function in otherFingerprint.functions:
            if function not in self.functions:
                diffs[function] = 1.
        sum = 0.
        for value in diffs.values():
            sum += value

        return 1-(sum / len(diffs.keys()))

fingerprints = {}
for i in os.listdir("output"):
    fprint = Fingerprint("output/" + i)

    if fprint is None:
        continue

    highest_diff_print = 0
    highest_diff = 0.0
    for f in fingerprints.keys():
        if highest_diff < fprint.compare_to(f):
            highest_diff_print = f.filename
            highest_diff = fprint.compare_to(f)

    print("%s\t%f\t%s" % (fprint.filename, highest_diff, highest_diff_print))
    fingerprints[fprint] = highest_diff
    
