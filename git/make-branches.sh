#!/bin/bash
for branch in `git branch -a | grep remotes | grep -v HEAD | grep -v master`
do
  $DEBUG git branch --track `echo $branch|sed 's-remotes/origin/--' ` $branch 
done

