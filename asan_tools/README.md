Overview
========

These tools are meant to help extract, parse, and filter crash logs from
ASAN-enabled applications. There are 3 stages total, with the first 2 being
built into one script, `asan_run.sh`.

Extraction
==========

Stage 1 is handled by `asan_run.sh`. It entails executing the application with
some set of arguments and checking for any ASAN report in the output. If it is
found, it passes the test case to the second stage, `asan_parse.py` which
executes the application a second time, this time capturing the output,
extracting any stack traces, and logging them to the specified CSV file.

Filtering
=========

The final stage involves using `asan_dedup.py` to remove duplicate stack traces
from the CSV file. This uses the Levenshtein distance algorithm to identify
stack traces that have 2 or less differing stack frames and removes one of them
as a duplicate.

Results
=======

These scripts were used on a test case corpus of around 40k files that were
passed into the ImageMagick `convert` tool.

Initial results showed 50k stacktraces. Final results after filtering duplicates
was approximately 150.
