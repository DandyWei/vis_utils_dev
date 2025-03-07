#!/bin/sh

# Navigate to the project directory
cd /D:/code/vis

# Initialize a new Git repository
git init

# Add all files to the repository
git add .

# Commit the changes
git commit -m "Initial commit"

# Replace 'your-repo-url' with the URL of your GitHub repository
git remote add origin your-repo-url

# Push the changes to the master branch
git push -u origin master
