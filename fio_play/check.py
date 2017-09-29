#!/usr/bin/python
#
# generate stats (average, mean, stddev and Pxx) from a flat list of samples
# in a file
#

import sys
import numpy


def check_samples(filename):
    with open(filename) as f:
        samples = map(lambda x: int(float(x)) , f.readlines())
        count = len(samples)
        samples.sort()

    print ("\"min\" : %d," % samples[0])
    print ("\"max\" : %d," % samples[-1])
    print ("\"mean\" : %d," % round(numpy.mean(samples), 2))
    print ("\"median\" : %d," % samples[count/2])
    print ("\"stddev\" : %d" % round(numpy.std(samples), 2))

    print("percentile : {")
    for i in range(10, 100, 5) + range (95, 100, 1):
        print ("  \"%d\" : %d," % (i, samples[count/100 * i]))
    for i in range(991, 1000, 1):
        print ("  \"99.%d\" : %d" % (i - 990, samples[count/1000 * i ]))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Calculates info on samples list.")
        print("Usage: check.py <samples_file>'")
        sys.exit(2)
    check_samples(sys.argv[1])