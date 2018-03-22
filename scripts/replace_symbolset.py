#! /bin/python

in_file_path = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/automata graph output/final.mnrl"
out_file_path = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/automata graph output/modified_final.mnrl"

in_file = open(in_file_path, 'r')
out_file = open(out_file_path, 'w')

dummy_symbolSet = "\"symbolSet\": \"[Dd]\""
for line in in_file:
  if "symbolSet" in line:
    start = line.find("symbolSet")
    start = line.find(": ", start) + 2
    line = line[:start] + "\"[Dd]\"\n"
    out_file.write(line)
  else:
    out_file.write(line)

in_file.close();
out_file.close();
