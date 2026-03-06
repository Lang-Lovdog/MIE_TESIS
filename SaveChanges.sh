#! bin/bash

# This is a hurry script which saves all changes to git
# The default message is the date and Hurry Changes string

git add .
git commit -m "Hurry changes $(date '+%Y-%m-%d %H:%M:%S')"
git push origin volky
