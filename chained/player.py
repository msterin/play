#!/usr/bin/env python3
#
# A player validating integrity and then stripping  the incoming file from hashes

# written by msterin@yahoo.com 12/14/2017


import argparse
import hashlib
import os
import tempfile

import const

def parse_args():
    '''Helper to parse arguments.'''
    p = argparse.ArgumentParser()
    p.add_argument('--source', help='Video file protected with hashes')
    p.add_argument('--hash', help='Head (block 0) hash file')
    return p

_test_fd = None # test hack - will save the file so we can compare
def stream_block(block):
    '''stub for actually showing the video, or streaming it somewhere'''
    # using this for a quick test (ugly hack)
    global _test_fd
    if _test_fd is None:
        _test_fd, name = tempfile.mkstemp(suffix=".tmp", text=False)
        print("TEST: Saving to {0}".format(name))
    os.write(_test_fd, block)

def process_file(source_name, hash_name):
    '''
    Open source_name and scan it while checking the hash
    Fails if integrity is not confirmed.
    Calls empty stub if all is OK
    '''
    with open(hash_name, "rb") as hash_fd:
        expected_digest = hash_fd.read()
    if len(expected_digest) != const.HASHSIZE:
        # something is bad
        raise RuntimeError('Wrong block0 hash size')

    print(expected_digest, len(expected_digest))

    with open(source_name, "rb") as source_fd:
        while True:
            block = source_fd.read(const.EXTENDEDSIZE)
            #print("block read {0}".format(len(block)))
            if len(block) == 0:
                break # we are done
            if len(block) == const.EXTENDEDSIZE:
                # calculate the hash for the block and check with expected_hash
                actual_digest = hashlib.sha256(block).digest()
                if actual_digest != expected_digest:
                    # TBD: give file position here
                    print("expected=", expected_digest, len(expected_digest))
                    print("  actual=", actual_digest, len(actual_digest))
                    raise RuntimeError('Hash mismatch. expect={0}, actual={1}'.\
                            format(expected_digest, actual_digest))
                # all good - remove the hash from the block and use as expected_hash
                expected_digest = block[const.BLOCKSIZE:]
                block = block[:-const.HASHSIZE]
            stream_block(block)


def main():
    '''parse the args and do the job'''
    parser = parse_args()
    args = vars(parser.parse_args())
    source_name = args["source"]
    hash_name = args["hash"]
    if source_name is None or hash_name is None:
        parser.parse_args(['--help'])
    process_file(source_name=source_name, hash_name=hash_name)

if __name__ == "__main__":
    main()