#!/bin/bash

# File containing the bash commands
filename="commands.txt"

# Loop through each line in the file and execute the command
while IFS= read -r command
do
  # Skip empty lines
  if [ -n "$command" ]; then
    echo "Executing: $command"
    eval "$command"
  fi
done < "$filename"