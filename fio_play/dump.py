#!/usr/bin/python
#
# dump bins info from FIO json+ output file to a flat file with a sample per line
#
# note: we assume only one job in FIO output. Otherwise, we'd need to select
# one we want to generate distribution for

#
# TBD - extract separare -read and -write files, and use them too.
#

import json
import sys

#
# fio_latency2csv.py
#
# This tool converts fio's json+ completion latency data to CSV format.
# For example:
#
# fio_latency2csv.py fio-jsonplus.output fio-latency.csv
#

import os
# import json
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('source',
                        help='fio json+ output file containing completion '
                             'latency data')
    parser.add_argument('dest',
                        help='destination file stub for latency data in CSV '
                             'format. job number will be appended to filename')
    args = parser.parse_args()

    return args


# from stat.c
def plat_idx_to_val(idx, FIO_IO_U_PLAT_BITS=6, FIO_IO_U_PLAT_VAL=64):
    # MSB <= (FIO_IO_U_PLAT_BITS-1), cannot be rounded off. Use
    # all bits of the sample as index
    if (idx < (FIO_IO_U_PLAT_VAL << 1)):
        return idx

    # Find the group and compute the minimum value of that group
    error_bits = (idx >> FIO_IO_U_PLAT_BITS) - 1
    base = 1 << (error_bits + FIO_IO_U_PLAT_BITS)

    # Find its bucket number of the group
    k = idx % FIO_IO_U_PLAT_VAL

    # Return the mean of the range of the bucket
    return (base + ((k + 0.5) * (1 << error_bits)))


if __name__ == '__main__':
    args = parse_args()

    with open(args.source, 'r') as source:
        jsondata = json.loads(source.read())

    bins = {}
    bin_const = {}
    ddir_list = ['read', 'write', 'trim']
    const_list = ['FIO_IO_U_PLAT_NR', 'FIO_IO_U_PLAT_BITS',
                  'FIO_IO_U_PLAT_VAL']

    for jobnum in range(0,len(jsondata['jobs'])):
        prev_ddir = None
        for ddir in ddir_list:
            bins[ddir] = jsondata['jobs'][jobnum][ddir]['clat']['bins']

            bin_const[ddir] = {}
            for const in const_list:
                bin_const[ddir][const] = bins[ddir].pop(const)
                if prev_ddir:
                    assert bin_const[ddir][const] == bin_const[prev_ddir][const]
            prev_ddir = ddir

        stub, ext = os.path.splitext(args.dest)
        outfile = stub + '_job' + str(jobnum) + ext

        with open(outfile, 'w') as output:
            for x in range(bin_const['read']['FIO_IO_U_PLAT_NR']):
                 lat = plat_idx_to_val(x,
                                       bin_const['read']['FIO_IO_U_PLAT_BITS'],
                                       bin_const['read']['FIO_IO_U_PLAT_VAL'])
                 for i in range(bins['write'][str(x)]):
                     output.write("{0}\n".format(lat))


# def extract_samples(fio_file, samples_file):
#     """
#     # Convert FIO histogram to samples list.
#     # FIO keeps it in bins: "{value: count, value: count"} .
#     # We need it (for ./maketable)  as a flat file with a single value per line
#     """

#     # open the file and extract bins
#     with open(fio_file, mode='r') as f:
#         data = json.load(f)
#     bins = data["jobs"][0]["write"]["clat"]["bins"]

#     # filter out values with 0 occurence
#     # '-3' is needed because there are 3 service lines in the bins
#     # so we have 3 less actual values to handle
#     occuring_values = filter(lambda x: bins[str(x)] != 0, range(len(bins)-3))

#     # Flatten the data into a list of individual samples
#     # e.g. {150:3} (meaning 150 msec latency was seen 3 times) will look like [150, 150, 150]
#     # and then print each sample as a separate line
#     with open(samples_file, mode='w') as f:
#         for value in occuring_values:
#             for sample in range(bins[str(value)]):
#                 f.writelines([str(value), "\n"])

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Convert FIO json+ output to a flat colums of samples.")
#         print("Usage: dump.py <fio_output> <samples_file>'")
#         sys.exit(2)
#     extract_samples(sys.argv[1], sys.argv[2])

