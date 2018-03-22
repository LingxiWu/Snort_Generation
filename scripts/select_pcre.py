#! /bin/python

import sys
import glob
import errno
import argparse
import re

#rules_path: /Snort/data/rules
parser = argparse.ArgumentParser(description="Go through Snort Rule set")
parser.add_argument("--rules_path", help="Path to directory holding Snort rules files.", required=True)
parser.add_argument("--regex_fn", help="Path to output file with extracted PCREs.", required=True)
args = parser.parse_args()

path = str(args.rules_path) + '/*.rules'
regex_fn = str(args.regex_fn)

"""
  Just a bunch of file i/o stuff for reading snort rulesets 
  and outputing converted regex.
"""
#snort_rulesets_path = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/rules_temp/" + "/*.rules"
#regex_results_file = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/regex/snort_regex.regex"

#input_files = glob.glob(snort_rulesets_path)
#output_file = open(regex_results_file, 'w')

input_files = glob.glob(path)
output_file = open(regex_fn, 'w')

# counter.
total_count = 0
for fn in input_files:

  f = open(fn, 'r')
  
  for line in f:  
    if "pcre:" in line:
      
      total_count += 1
      
      # read a PCRE line.
      start = line.find("pcre:")
      start = line.find("/", start - 1)
      end = line.find("\";", start, len(line))
      pcre_line = line[start:end]

      output_file.write(pcre_line + "\n")

  f.close()

print("\n--- summmary from select_pcre.py ---")
print("total_pcre_extracted: ", total_count)
print("--- end ---")