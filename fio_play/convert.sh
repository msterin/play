#!/bin/bash
#
# Generate distribution table and stats info from FIO historgram bucket info.
# The resulting table is used to generate distribution similar to the one observed by FIO
# for now, manually configure stuff

# tools used:
tooldir=`dirname $0`
dump="$tooldir/dump.py"       # dump FIO json+ histogam bins to a list of individual samples
maketable="$tooldir/maketable" # from iproute2/netem. Generates dist.tables
stats="$tooldir/stats" # from iproute2/netem. Calculates mean/deviation

fio_file="$1"
if [ "$fio_file" == "" ]
then
    echo Usage: convert.sh file_with_fio_info
    exit 2
fi


echo generating samples from $fio_file...
samples=`tempfile`
$dump $fio_file $samples

fio_base="${fio_file%.*}" # strip suffix
stats_file=$fio_base.stats
dist_file=$fio_base.dist_table

echo generating dist and stats \($dist_file and $stats_file\)
$stats $samples > $stats_file
$maketable $samples > $dist_file
rm $samples
