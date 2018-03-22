#!/bin/bash

# DEFAULT_MNRL_FILES=/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/giant_copy/*.mnrl

#
# Iterate through all .mnrl files and gather stats
# Output to a .txt file.
#

declare -i number
number=0

MNRL_FILES=/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/giant/*.mnrl
for f in $MNRL_FILES
do

  result=$(/zf18/lw2ef/Documents/workspace/VASim/vasim -Ox $f | egrep -o "([0-9]*.mnrl$)|(STEs: [0-9]*)|(Max Fan-in \(not including self loops\): [0-9]+)|(Max Fan-out \(not including self loops\): [0-9]+)|(Average Node Degree: ([0-9]*[.])?[0-9]+)|(Compressability: ([0-9]*[.])?[0-9]+)")
  
  echo "$result" >> filtered_output.txt
  
  ((number++))

done

echo "Number = $number"

