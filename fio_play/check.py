#!/usr/bin/python
#
# generate stats (average, mean, stddev and Pxx) from a flat list of samples
# in a file
#

import sys

def check_samples(filename):
   with open(filename) as f:
      samples = map(lambda x: int(x) , f.readlines())
      count = len(samples)
   average = reduce(lambda x, y: x + y, samples)/count
   print ("Average", average)
   for i in range (10, 101, 5):
      print ("P%d : %d", (i, samples[count/100 * i ]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Calculates info on samples list.")
        print("Usage: check.py <samples_file>'")
        sys.exit(2)
    check_samples(sys.argv[1])