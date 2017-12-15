#!/usr/bin/env python3
#
# An encoder that receives a file and creates the hash-protected version of the file, as well as the
# hex string of h 0 (exactly 64 hex digits).
#
# this version does only one pass on source read
# written by msterin@yahoo.com 12/14/2017

import hashlib
import argparse
import os
import os.path
import fallocate
import sys

import const

DEFAULT_OUT_SUFFIX = ".out"
DEFAULT_HASH_SUFFIX = ".hash"

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


def get_target_block_location(block_start):
    '''Given the block start in source, find out where does it land in target
    '''
    if block_start == 0:
        return block_start

    count = int(block_start / const.BLOCKSIZE)
    return block_start + count * const.HASHSIZE

def process_file(source_name, out_name, hash_name):
    '''open file and do the work'''

    # TBD: yell if size is too small
    # TBD: check there is no override
    # TBD: get better error handling
    source_fd = open(source_name, "rb")
    out_fd = open(out_name, "wb")
    hash_fd = open(hash_name, "wb")

    # start of the last block
    size = os.stat(source_name).st_size
    if size == 0:
        print("Empty file, nothing to do")
        sys.exit()
    block_start = int((size - 1)/const.BLOCKSIZE) * const.BLOCKSIZE

    out_size = size + int((size + 1)/const.BLOCKSIZE) * const.HASHSIZE
    print("size", size)
    print("couint", int((size + 1)/const.BLOCKSIZE))
    print("Out size is {0}".format(out_size))
    fallocate.fallocate(out_fd, 0, out_size)

    current_hash = None

    # scan the source file while building hashes, but write hash in the proper location
    while True:
        source_fd.seek(block_start)
        #print("setting position to {0}".format(block_start))
        block = source_fd.read(const.BLOCKSIZE)
        out_loc = get_target_block_location(block_start)
        out_fd.seek(out_loc)
        out_fd.write(block)
        if current_hash is not None:
            block += current_hash.digest()
        # calculate and save the hash, and move to the prior block
        current_hash = hashlib.sha256(block)
        # write out hash
        if out_loc == 0:
            # first block. just save hash in a dedicated file and we are done
            hash_fd.write(current_hash.digest())
            break
        else:
            #save hash in the target file
            out_fd.seek(out_loc - const.HASHSIZE)
            out_fd.write(current_hash.digest())
        block_start -= const.BLOCKSIZE
    # close - we are done
    source_fd.close()
    out_fd.close()
    hash_fd.close()


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

