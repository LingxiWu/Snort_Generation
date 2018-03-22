#! /bin/python

file_path = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/scripts/old_snort_regex.txt"

old_snort_regex_file = open(file_path, 'r')

old_snort_regex_set = set()

for line in old_snort_regex_file:
  old_snort_regex_set.add(line)
  
old_snort_regex_file.close()  

print(len(old_snort_regex_set))
