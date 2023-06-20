#!/bin/bash

FILES="Data_Latest/*"
for f in $FILES
do
    echo "Processing $f file..."
    # take action on each file. $f store current file name
    # cat "$f"
    python Preprocess/split_by_week.py $f Mentions_By_Week -f
done