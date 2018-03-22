#!/bin/python

import sys
import glob
import errno
import argparse
import re

#parser = argparse.ArgumentParser(description='Extract PCRE regular expressions from Snort rule files.')
#parser.add_argument('--rules_path', help='Path to directory holding Snort rules files.', required=True)
#parser.add_argument('--regex_fn', help='Path to output file with extracted pcres.', required=True)
#args = parser.parse_args()

#path = str(args.rules_path) + '/*.rules'
#regex_fn = str(args.regex_fn)

snort_rulesets_path = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/rules_temp/" + "/*.rules"
regex_results_file = "/zf18/lw2ef/Documents/workspace/ANMLZoo2/Snort/Snort_debug/regex/snort_regex.regex"

#files = glob.glob(path)
#regex_file = open(regex_fn, 'w')

files = glob.glob(snort_rulesets_path)
regex_file = open(regex_results_file, 'w')

good = 0
unsupported_modifier = 0
backrefs = 0
bad_anchors = 0
weirdos = 0

for fn in files:

    f = open(fn, 'r')

    for line in f:
        if "pcre:" in line :
            start = line.find("pcre:")
            start = line.find("/", start - 1)
            end = line.find("\";", start, len(line))
            
            if line[start:end].startswith('/|') :
                weirdos = weirdos + 1
                #sys.stdout.write("Unsupported PCRE WEIRDO: ")
                #sys.stdout.write(line[start:end] + "\n")	
                continue

            if line[start:end].endswith('|/') :
                weirdos = weirdos + 1
                #sys.stdout.write("Unsupported PCRE WEIRDO: ")
                #sys.stdout.write(line[start:end] + "\n")             
		continue

            if "(?" in line :
                backrefs = backrefs + 1
                #sys.stderr.write("Unsupported PCRE BACKREF ?: ")
                #sys.stderr.write(line[start:end] + "\n")
                continue

            p = r'\\\d'
            m = re.search(p, line[start:end])
            if m:
                backrefs = backrefs + 1
                #sys.stderr.write("Unsupported PCRE BACKREF: ")
                #sys.stderr.write(line[start:end] + "\n")
                continue


            if "|$)" in line :
                bad_anchors = bad_anchors + 1
                #sys.stderr.write("Unsupported PCRE END ANCHOR: ")
                #sys.stderr.write(line[start:end] + "\n")
                continue

            # for each "^" in the line
            p = r'[^\[]\^'
            m = re.search(p, line[start+1:end])
            if m:
                bad_anchors = bad_anchors + 1
                #sys.stderr.write("Unsupported PCRE START ANCHOR: ")
                #sys.stderr.write(line[start:end] + "\n")
                continue


            #sys.stdout.write(line[start:end] + "\n")
            regex_file.write(line[start:end] + "\n")

    f.close()

print "Expressions excluded due to modifiers: " + str(unsupported_modifier)
print "Expressions excluded due to backrefs: " + str(backrefs)
print "Expressions excluded due to embedded anchors: " + str(bad_anchors)
print "Expressions excluded due to weirdos: " + str(weirdos)
regex_file.close()
