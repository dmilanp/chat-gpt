#!/bin/bash

# Check if DIARY_DIR environment variable is set
if [[ -z "${DIARY_DIR}" ]]; then
  echo "Error: DIARY_DIR environment variable is not defined."
  exit 1
fi

# Get the current date in YYYY-MM-DD format
datestamp=$(date +"%Y-%m-%d")
timestamp=$(date +"%I:%M %p")


# Check if there are any entries in the diary file for the current date
if grep -q "^$datestamp$" "${DIARY_DIR}/diary.txt"; then
  # If there are already entries for the current date, just append the new entry with a timestamp
  echo -e "\n$timestamp\n$*" >> "${DIARY_DIR}/diary.txt"
else
  # If it's a new date, append the date and timestamp along with the new entry
  echo -e "\n\n$datestamp\n\n$timestamp\n$*" >> "${DIARY_DIR}/diary.txt"
fi

# Print a confirmation message
echo "Entry saved to diary."
