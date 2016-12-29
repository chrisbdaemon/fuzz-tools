Coverage Collection Tools

Note: All paths are hardcoded. They will need to be changed before use.

lcov-reset.sh
Recursive reset of all coverage data collected thus far. Takes no arguments,
resets all in the current directory.

lcov-run-testcases-hourly.py
This Python script is designed to execute the code coverage command (again,
hardcoded in the script, will need to modify) for all test cases in a given
directory and create hourly results based on the last-access date for each test
case.
