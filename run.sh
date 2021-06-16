#!/bin/bash

# Please remember to use chmod +x run.sh to make this executable

# This is the requested run.sh. It makes sure the program has everything it requires
# to begin. It downlads the required dependencies if they cannot be found. 

# Check params

if [ "$#" -ne 1 ] || ! [ -f "$1" ]; then
  echo "Usage: sh run.sh FILENAME" >&2
  exit 1
fi

# Run python

echo "Checking dependencies..."

# Check the virtual environment exists, and create it if it doesnt
if [ ! -d ".venv" ] 
then
    echo "The virtual environment does NOT exist. Proceeding to create it"


    # Python command to create the virtual env
    python3 -m virtualenv .venv


    echo "Installing dependencies in the virtual environment"
    # Activate and download the jinja modules
    source .venv/bin/activate
    pip install -r requirements.txt
fi


# Initialize the virtual env
source .venv/bin/activate

python3 slr.py $1