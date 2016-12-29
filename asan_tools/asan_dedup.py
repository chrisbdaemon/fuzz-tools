#!/usr/bin/env python3

import argparse
import csv
import sys


class StackFrame:
    def __init__(self, address, symbol, source):
        self.address = address
        self.symbol = symbol
        self.source = source

    def __repr__(self):
        return "<StackFrame address=%s symbol='%s' source='%s'>" % (
            self.address, self.symbol, self.source)

    def is_different(self, other):
        if self.symbol == other.symbol and self.source == other.source:
            return False
        else:
            return True


class StackTrace:
    def __init__(self, filename, raw_frames):
        self.filename = filename
        self.frames = []

        address = None
        symbol = None
        source = None
        for i, frame_element in enumerate(raw_frames):
            if i % 3 == 0:
                address = frame_element
            elif i % 3 == 1:
                symbol = frame_element
            elif i % 3 == 2:
                source = frame_element
                frame = StackFrame(address, symbol, source)
                self.frames.append(frame)

    def __repr__(self):
        return "<StackTrace filename='%s' frames=%s>" % (self.filename, self.frames)

    def distance(self, other):
        matrix = []
        for i in range(len(self.frames)+1):
            row = []
            for j in range(len(other.frames)+1):
                row.append(0)
            matrix.append(row)

        for i in range(len(self.frames)+1):
            matrix[i][0] = i
        for i in range(len(other.frames)+1):
            matrix[0][i] = i

        for y in range(len(matrix)-1):
            y += 1
            for x in range(len(matrix[y-1])-1):
                x += 1
                cost = 0
                if len(self.frames) < i or len(other.frames) < j:
                    cost = 1
                elif self.frames[y-1].is_different(other.frames[x-1]):
                    cost = 1

                matrix[y][x] = min(matrix[y-1][x] + 1, matrix[y][x-1] + 1, matrix[y-1][x-1] + cost)
        return matrix[-1][-1]


def printMatrix(matrix):
    for i in matrix:
        for j in i:
            sys.stdout.write("%2d " % j)
        print("")


def main():
    parser = argparse.ArgumentParser(
        description='remove duplicates from asan results')
    parser.add_argument('filename', nargs=1, type=str,
                        help='filename of CSV file')
    args = parser.parse_args()
    csv_filename = args.filename[0]

    traces = []

    fd = open(csv_filename, "r")
    csv_reader = csv.reader(fd)
    for i, row in enumerate(csv_reader):
        print("%d:%d" % (i+1, len(traces)))
        test_case_filename = row[0]
        frames = row[4:]
        new_trace = StackTrace(test_case_filename, frames)

        dup = False
        for j, trace in enumerate(traces):
            if trace.distance(new_trace) <= 2:
                dup = True
                break
        if not dup:
            traces.append(new_trace)

    for t1 in traces:
        print(t1.filename)

if __name__ == '__main__':
    main()
