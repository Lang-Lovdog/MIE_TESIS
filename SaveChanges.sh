#!/bin/bash

# This is a hurry script which saves all changes to git
# The default message is the date and Hurry Changes string

commit_message=""
if [ $# -gt 1 ]; then
  for i in "$@"; do
    commit_message="$commit_message $i"
  done
else
  commit_message="Hurry changes $(date '+%Y-%m-%d %H:%M:%S')"
fi

git add .
git commit -m "$commit_message"
git push origin volky
