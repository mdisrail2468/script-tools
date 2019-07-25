#!/bin/bash


lrepo=$(find . -type d -name .git)
pwd=$(pwd)

for r in $lrepo ; do
	rr=$(dirname $r)
	cd $rr
	{


		find .git/objects/pack/ -name "*.idx" |
		while read i ; do
			git show-index < "$i" | awk '{print $2}';
		done;
	
		find .git/objects/ -type f | grep -av '/pack/' | awk -F '/' '{print $(NF-1)$NF}';
	} | while read o ; do echo $o; git cat-file -p $o; done | grep --color -aiE $1
	cd $pwd
done
