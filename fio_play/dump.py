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

def extract_samples(fio_file, samples_file):
    """
    # Convert FIO histogram to samples list.
    # FIO keeps it in bins: "{value: count, value: count"} .
    # We need it (for ./maketable)  as a flat file with a single value per line
    """

    # open the file and extract bins
    with open(fio_file, mode='r') as f:
        data = json.load(f)
    bins = data["jobs"][0]["write"]["clat"]["bins"]

    # filter out values with 0 occurence
    # '-3' is needed because there are 3 service lines in the bins
    # so we have 3 less actual values to handle
    occuring_values = filter(lambda x: bins[str(x)] != 0, range(len(bins)-3))

    # Flatten the data into a list of individual samples
    # e.g. {150:3} (meaning 150 msec latency was seen 3 times) will look like [150, 150, 150]
    # and then print each sample as a separate line
    with open(samples_file, mode='w') as f:
        for value in occuring_values:
            for sample in range(bins[str(value)]):
                f.writelines([str(value), "\n"])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Convert FIO json+ output to a flat colums of samples.")
        print("Usage: dump.py <fio_output> <samples_file>'")
        sys.exit(2)
    extract_samples(sys.argv[1], sys.argv[2])

