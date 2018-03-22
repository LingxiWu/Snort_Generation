#! /bin/python

import sys
import glob
import errno
import argparse
import re

# rules_path: /Snort/data/rules
parser = argparse.ArgumentParser(description="A small step toward succesfull PCRE regex extraction.")
# parser.add_argument("--rules_path", help="Path to directory holding Snort rules files.", required=True)
# parser.add_argument("--regex_fn", help="Path to output file with extracted PCREs.", required=True)
args = parser.parse_args()

# path = str(args.rules_path) + "/*.rules"
path = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/rules_temp/" + "/*.rules"
regex_results = "Snort/Snort_debug/regex_results"
files = glob.glob(path)


#f = open(single_rule_file, 'r')
#count = 0

def mod_info():
  """
  Use dictionary to store modifiers and their occurrence for Snort ruleset.
  """
  mod_dict = {}
  for fn in files:
  
    f = open(fn, 'r')
    
    for line in f:  
  
      if "pcre:" in line:
	start = line.find("pcre:")
	start = line.find("/", start - 1)
	end = line.find("\";", start, len(line))
	pcre_line = line[start:end]
	#print(pcre_line)
	pcre_line = line[start:end]
	mod_idx = pcre_line.rfind("/")+1
	#print(mod_idx)
	modifier = pcre_line[mod_idx:end]

	mod_dict[modifier] = mod_dict.get(modifier, 0) + 1
	
    f.close()
    
  return mod_dict

"""
Try a single file:
app-detect.rules. See if it works
"""

#single_rule_file = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/data/rules/app-detect.rules"  
single_output_file = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/regex/single_output_regex.regex"

###########################
common_prefix = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/regex/"

or_file = common_prefix + "or_file.regex"
bak_ref_q = common_prefix + "bak_ref_q.regex"
bak_ref_slash = common_prefix + "bak_ref_slash.regex"
bad_start_anchor = common_prefix + "bad_start_anchor.regex"
bad_end_anchor = common_prefix + "bad_end_anchor.regex"

###########################

#input_f = open(single_rule_file, 'r')
output_f = open(single_output_file, 'w')

output_or_file = open(or_file, 'w')
bak_ref_q_file = open(bak_ref_q, 'w')
bak_ref_slash_file = open(bak_ref_slash, 'w')
bad_start_anchor_file = open(bad_start_anchor, 'w')
bad_end_anchor_file = open(bad_end_anchor, 'w')

# various counters.
total_count = 0
back_ref_slash_count = 0
back_ref_question_count = 0
bad_end_anchor_count = 0
bad_start_anchor_count = 0
or_count = 0
total_passed_count = 0

index = 0
for fn in files:

  f = open(fn, 'r')
  
  for line in f:  
    if "pcre:" in line:
      
      total_count += 1
      
      # read a PCRE line.
      start = line.find("pcre:")
      start = line.find("/", start - 1)
      end = line.find("\";", start, len(line))
      pcre_line = line[start:end]
      
      
      p = re.compile(r"[^\[]\^") # fun fact: [^..] means exclude the following...l
      m = p.findall(pcre_line)
      if len(m)>0:
	bad_start_anchor_count = bad_start_anchor_count + 1
	#print(str(total_count)+": "+pcre_line)
	#print(m)
	bad_start_anchor_file.write(pcre_line + "\n")
	continue
      
      if "(?" in line:
	back_ref_question_count += 1
	#print(str(total_count)+": "+pcre_line)
	bak_ref_q_file.write(pcre_line + "\n")
        continue   
      
      if pcre_line.startswith('/|'):
	or_count += 1
	#print(str(total_count)+": "+pcre_line)
	output_or_file.write(pcre_line + "\n")
        continue
      
      if pcre_line.endswith('|/'):
	# exclude the case: '\|/'
	if pcre_line[len(pcre_line)-3] != '\\':
	  output_or_file.write(pcre_line + "\n")
	  or_count += 1
	  continue
            
      if "|$)" in line :
	bad_end_anchor_count = bad_end_anchor_count + 1
	#print(str(total_count)+": "+pcre_line)
	bad_end_anchor_file.write(pcre_line + "\n")
        continue
     
      
      
        
      p = re.compile(r"\\\d")
      m = p.findall(pcre_line)
      if len(m)>0:
	back_ref_slash_count += 1
	#print(str(total_count)+": "+pcre_line)
	#print(m)
	bak_ref_slash_file.write(pcre_line + "\n")
	continue
##########################################        
      #p = r"\\\d"
      #m = re.search(p, pcre_line)
      #if m:
	#back_ref_slash_count += 1
	#print(pcre_line+"\n")
	#continue
##########################################
      total_passed_count += 1
      #output_f.write(str(total_passed_count) + ": " + pcre_line + "\n")
      output_f.write(pcre_line + "\n")

  f.close()
  #output_f.write("======================" + "\n")
#output_f.close()
print("\n--- summmary ---")
print("total_count: ", total_count)
print("or_count: ", or_count)
print("back_ref_slash_count: ", back_ref_slash_count)
print("back_ref_question_count: ", back_ref_question_count)
print("bad_start_anchor_count: ", bad_start_anchor_count)
print("bad_end_anchor_count: ", bad_end_anchor_count)
print("total_passed_count: ", total_passed_count)
print("--- end ---")