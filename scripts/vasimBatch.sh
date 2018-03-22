#!/bin/bash

# DEFAULT_MNRL_FILES=/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/giant_copy/*.mnrl

#
# Iterate through all .mnrl files and identify troubled ones.
# Output 
#
MNRL_FILES=/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/giant/*.mnrl
for f in $MNRL_FILES
do
  if /zf18/lw2ef/Documents/workspace/VASim/vasim -a $f | grep -q "Automata Statistics" 
    then :
    else 
      /zf18/lw2ef/Documents/workspace/VASim/vasim -a $f | grep --line-buffered "Building automata from file:" |tee -a filtered_output.txt 
  fi
done

