#!/bin/sh

for filename in $1/*; do
	outfile=$2/$(basename "$filename").pcap
	echo "Encapsulating ${filename}"
	od -Ax -tx1 -v ${filename} | text2pcap -q - $outfile
done
