# Helper to clean up git repos

The web page "how to shrink a git repo": http://stevelorek.com/how-to-shrink-a-git-repository.html

It is the base for micro-scripts used.

The sequence of work is explained in the page. scripts are just cut-n-paste code and slight
change of format (so you can run `DEBUG=echo <script>` to just print command), and also
to play with the list of removed stuff.

But basically, you can just follow the page.

First, go to your where your repo is checked out.
I assume this folder is ../play/git relative to your repo.

## Check the effort is worth your time

This is our repo "before"

```bash
$ pwd
~/workspace/backups/ss-pop-agent
$ du -sh .git .
 289M	.git
 343M	.
```



## Make local branches

Create local tracking branches from remote so clean up scrips can traverse them

```bash
../play/git/make-branches.sh
```

# Find large files

So it is clear what to clean up. I used that

```bash
../play/git/find-large.sh | tail +3 | awk '{print $4}' > pop_useless_files.txt
```

## Review the list, out of paranoia

I removed something I *thought* might be still useful from the list, manually, with vi.

## Clean the files and reclaim space them from git

```bash
../play/git/filter.sh
../play/git/git-prune.sh
```

filter is separated from prune so you can fine tune and experiment with what's removed.

Note - the script has hardcoded filename for the list, needs to change to param

## Check the size, Push back to repo

After the change:

```bash
$ pwd
~/workspace/ss-pop-agent
$ du -sh .git .
 13M	.git
 57M	.
```

push:

```
../play/git/push-back.sh
```

## Update the team

Everyone needs to `git fetch -a -p` and `git rebase origin/master` on their branches,
before any push.