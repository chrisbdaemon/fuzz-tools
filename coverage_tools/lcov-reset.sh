#!/usr/bin/bash

find . -type d -exec lcov --directory . --zerocounters \;
