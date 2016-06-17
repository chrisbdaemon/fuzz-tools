#!/usr/bin/bash

for filename in $1/*; do
	timeout 5 /home/chris/NIST/chroot/1.12.8/bin/tshark -nxVr $filename
	retval=$?
	if [[ $retval -eq 124 ]]; then
		echo $filename >> loops.txt
		exit
	fi
done
