#!/bin/bash

if [ $# -ne 3 ]; then
	echo "Usage: $0 <input dir> <output_dir> <pkt_count>"
	exit -1
fi

in_dir=$1
out_dir=$2
pkt_c=$3

tmp_out_dir="/tmp/tmp_pcap"
mkdir -p $tmp_out_dir
for pcap_file in $(find $in_dir -name "*.pcap"); do
	if [[ ! -z $(editcap -c $pkt_c $pcap_file $tmp_out_dir/pcap_ 2>&1) ]]; then
		echo "Unable to split corrupt pcap: $pcap_file"
	fi

	for s_pcap_file in $(ls $tmp_out_dir); do
		hash=`sha256sum $tmp_out_dir/$s_pcap_file | cut -d ' ' -f 1`
		prefix=$(($((16#${hash:0:2})) % 8))

		if [ ! -d $out_dir/$prefix ]; then
			mkdir -p $out_dir/$prefix
		fi

		mv $tmp_out_dir/$s_pcap_file $out_dir/$prefix/$hash.pcap
	done
	rm -rf $tmp_out_dir/*
done
