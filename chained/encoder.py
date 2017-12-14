#!/usr/bin/env python3
#
# An encoder that receives a file and creates the hash-protected version of the file, as well as the
# hex string of h 0 (exactly 64 hex digits).
#
# written by msterin@yahoo.com 12/14/2017


import hashlib
import argparse
import os
import os.path

DEFAULT_OUT_SUFFIX = ".out"
DEFAULT_HASH_SUFFIX = ".hash"

BLOCKSIZE = 1024 # a chunk of file covered with a single hash

def parse_args():
    '''Helper to parse arguments.'''
    p = argparse.ArgumentParser()
    p.add_argument('--source', help='Video file to protect with hashes')
    p.add_argument('--out_suffix',
        help='Suffix for output. Default is {0}'.format(DEFAULT_OUT_SUFFIX),
        default=DEFAULT_OUT_SUFFIX)
    p.add_argument('--hash_suffix',
        help='Suffix for hash file. Default is {0}'.format(DEFAULT_HASH_SUFFIX),
        default=DEFAULT_HASH_SUFFIX)
    return p

def process_file(source_name, out_name, hash_name):
    '''open file and do the work'''

    # TBD: yell if size is too small
    # TBD: check there is no override
    # TBD: get better error handling
    source_fd = open(source_name, "rb")
    out_fd = open(out_name, "wb")
    hash_fd = open(hash_name, "wb")

    # start of the last block
    block_end = os.stat(source_name).st_size
    block_start = int((block_end - 1)/BLOCKSIZE) * BLOCKSIZE
    # size of the block to process
    size = block_end - block_start

    # read the source backwards and construct array of hashes. Simply insert the
    # next one into start of the array
    hash = None
    hashes = [None] # We'll use it to indicate the last block
    while block_start >= 0:
        source_fd.seek(block_start)
        print("setting position to {0} {1} {2}".format(block_start, block_end, size))
        block = source_fd.read(size)
        if hash is not None:
            block += hash.digest()
        hash = hashlib.sha256(block)
        print(hash.hexdigest())
        hashes.append(hash)
        size = BLOCKSIZE
        block_start -= BLOCKSIZE

    # now 'hash' is the hash for the first block. Spit it out and forget
    hash_fd.write(hash.digest())
    hashes.pop()
    # and reverse, so the hashes in the array are aligned with blocks they go to
    # notice that #0 there is hash for Block1 (which goes into Block 0) and the
    # last is None, which is exactly what goes to the last block
    hashes.reverse()

    # now copy the source while adding hash.
    # we know exactly how many blocks are there...
    source_fd.seek(0)
    for hash in hashes:
        block = source_fd.read(BLOCKSIZE) # the last one simply reads less
        if hash is not None:
            block += hash.digest()
        print("writeing block with hash, len {0}".format(len(block)))
        out_fd.write(block)




def main():
    '''parse the args and do the job'''
    parser = parse_args()
    args = vars(parser.parse_args())
    source_name = args["source"]
    if source_name is None:
        parser.parse_args(['--help'])
    out_name = os.path.splitext(source_name)[0] + args["out_suffix"]
    hash_name = os.path.splitext(source_name)[0] + args["hash_suffix"]
    process_file(source_name=source_name, out_name=out_name, hash_name=hash_name)

if __name__ == "__main__":
    main()

