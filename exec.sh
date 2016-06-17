#!/usr/bin/env bash

LD_LIBRARY_PATH=/home/chris/NIST/chroot/lib

for pcap_file in pcaps/*; do
	timeout 5 /home/chris/NIST/chroot/bin/tshark -nxVr ${pcap_file}
	rv=$?
	echo RV: ${rv}
	if [ ${rv} == 124 ]; then
		echo ${pcap_file} >> loops.txt
	fi

	if [ ${rv} == 139 ]; then
		echo ${pcap_file} >> segfaults.txt
	fi
done
