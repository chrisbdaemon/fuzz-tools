#!/usr/bin/bash

for filename in $(find $1 -type f -wholename "*crashes*"); do
	hash=$(sha256sum $filename | cut -d " " -f 1)
	cp -v $filename crashes/$hash
done
