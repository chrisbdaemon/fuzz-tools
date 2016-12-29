#!/usr/bin/env python3

import argparse
import csv
import sys
import re
import subprocess
import copy


def classify_output(output):
    for line in output.split("\n"):
        m = re.search(r"==\d+==(\S+): (.+)", line)
        if m is None:
            continue

        classification = m.groups()[0]
        message = m.groups()[1]
        return {'class': classification, 'message': message}

    return None


def parse_stacks(output):
    in_stacktrace = False
    stacktraces = []

    # strip asan header
    m = re.search(r"==\d+==.*\n", output)
    output = output[m.end():]

    curr_stacktrace = {'header': '', 'frames': []}
    for line in output.split("\n"):
        line = line.strip()

        if "libsanitizer" in line:
            continue

        if len(line) == 0:
            if in_stacktrace:
                stacktraces.append(curr_stacktrace)
                in_stacktrace = False
                curr_stacktrace = {'header': '', 'frames': []}
            continue

        in_stacktrace = True

        match = re.search(r"^\W+(\d+) (0x\w+) in (\w+) \(?(.+)\)?$", line)
        if match is None:
            curr_stacktrace['header'] += " " + line
            continue

        matchGroups = match.groups()
        stackframe = {}
        stackframe["address"] = matchGroups[1]
        stackframe["function"] = matchGroups[2]
        stackframe["location"] = matchGroups[3]

        curr_stacktrace['frames'].append(stackframe)

    return stacktraces


def write_to_csv(csvfile, filename, classification, stacktraces):
    logEntries = []
    baseLogEntry = []
    baseLogEntry.append(filename)
    baseLogEntry.append(classification['class'])
    baseLogEntry.append(classification['message'])
    for stacktrace in stacktraces:
        logEntry = copy.deepcopy(baseLogEntry)
        logEntry.append(stacktrace['header'])
        for frame in stacktrace['frames']:
            logEntry.append(frame['address'])
            logEntry.append(frame['function'])
            logEntry.append(frame['location'])
        logEntries.append(logEntry)

    csvfile.writerows(logEntries)


def main():
    parser = argparse.ArgumentParser(
        description='execute command, parse any ASAN output into CSV file')
    parser.add_argument('output', nargs=1, type=str, help='CSV filename')
    parser.add_argument('command', nargs=1, type=str, help='command to execute')
    args = parser.parse_args()

    cmd = " ".join(args.command)

    logfile = open(args.output[0], "a+")
    csvfile = csv.writer(logfile)
    try:
        out = subprocess.getoutput(cmd)
        classification = classify_output(out)
        if classification is not None:
            stacktraces = parse_stacks(out)
            write_to_csv(csvfile, cmd, classification, stacktraces)
            print(classification['class'])

    except UnicodeDecodeError:
        pass
    logfile.close()

if __name__ == "__main__":
    main()
