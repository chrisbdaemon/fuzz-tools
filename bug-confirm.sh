#!/usr/bin/env bash

LD_LIBRARY_PATH=/home/chris/NIST/chroot/lib
EXEC_CMD=/home/chris/NIST/chroot/bin/tshark -nxVr 

for file in pcaps/*; do
	timeout 5 /home/chris/NIST/chroot/bin/tshark -nxVr ${file}
	timeout 5 ${EXEC_CMD} ${file}
	rv=$?
	echo RV: ${rv}
	if [ ${rv} == 124 ]; then
		echo ${file} >> loops.txt
	fi

	if [ ${rv} == 139 ]; then
		echo ${file} >> segfaults.txt
	fi
done
