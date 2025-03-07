#!/bin/sh

# Navigate to the project directory
cd /D:/code/vis

# Fetch the latest changes from the remote repository
git fetch origin

# Force merge the master branch with unrelated histories
git merge origin/master --allow-unrelated-histories
