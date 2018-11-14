#!/bin/bash
set -x

list=$(cat ../play/git/pop_useless_files.txt | tr '\n' ' ' )

#for item in $list
#do
#  $DEBUG git filter-branch --tag-name-filter cat --index-filter "git rm -r --cached --ignore-unmatch $item" --prune-empty -f -- --all
#done

$DEBUG git filter-branch --tag-name-filter cat --index-filter "git rm -r --cached --ignore-unmatch $list" --prune-empty -f -- --all


