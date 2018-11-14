#!/bin/sh

set -x
# push the changes back to the remote repository, so that nobody else will suffer the pain of a 400MB download.
$DEBUG git push origin --force --all

# and, in adition to commits. push the new tags back
$DEBUG git push origin --force --tags

set +x
