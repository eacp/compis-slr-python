#!/bin/sh

# Please remember to use chmod +x run.sh to make this executable

# Check params

if [ "$#" -ne 1 ] || ! [ -f "$1" ]; then
  echo "Usage: sh run.sh FILENAME" >&2
  exit 1
fi

# Run python

python3 slr.py $1