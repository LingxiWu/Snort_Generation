#! /bin/python
import re
import operator
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

#help(plt.hist)

snort_stats_file = "filtered_output.txt"

# mnrl that could not be compressed
failed_to_compress = []

# maps
pre_ste_dict = {}
post_ste_dict = {}

pre_fan_in_dict = {}
post_fan_in_dict = {}

pre_fan_out_dict = {}
post_fan_out_dict = {}

pre_node_degree_dict = {}
post_node_degree_dict = {}

compressability_dict = {}

i = 0
prev_mnrl_id = ""
cur_mnrl_id = ""

# make a list of failed_to_compress mnrls
f = open(snort_stats_file, 'r')
for line in f:
  if ".mnrl" in line:
    prev_mnrl_id = cur_mnrl_id
    cur_mnrl_id = line
    if i == 1:
      i = 0
    elif prev_mnrl_id != "" and i == 0:
      failed_to_compress.append(prev_mnrl_id.rstrip())
    continue
  if "Compressability" in line:
    i += 1

f.close()

#print("failed to optimize")
#print(failed_to_compress)

f = open(snort_stats_file, 'r')
j = 0
k = 0
for line in f:
  if ".mnrl" in line:
    j = 1
    k = 0
    mnrl_id = line.rstrip()
    continue;
  
  elif "STEs" in line:
    if j == 1:
      pre_ste_dict.update({mnrl_id:int(re.findall(r"\d+", line)[0])})
    elif j == 2:
      post_ste_dict.update({mnrl_id:int(re.findall(r"\d+", line)[0])})
    k += 1
      
  elif "Max Fan-in" in line:
    if j == 1:
      pre_fan_in_dict.update({mnrl_id:int(re.findall(r"\d+", line)[0])})
    elif j == 2:
      post_fan_in_dict.update({mnrl_id:int(re.findall(r"\d+", line)[0])})
    k += 1
    
  elif "Max Fan-out" in line:
    if j == 1:
      pre_fan_out_dict.update({mnrl_id:int(re.findall(r"\d+", line)[0])})
    elif j == 2:
      post_fan_out_dict.update({mnrl_id:int(re.findall(r"\d+", line)[0])})
    k += 1
    
  elif "Average Node Degree" in line:
    if j == 1:
      pre_node_degree_dict.update({mnrl_id:float(re.findall(r"\d+\.\d+|\d", line)[0])})
    elif j == 2:
      post_node_degree_dict.update({mnrl_id:float(re.findall(r"\d+\.\d+|\d", line)[0])})
    k += 1

  elif "Compressability" in line:
    compressability_dict.update({mnrl_id:float(re.findall(r"\d+\.\d+|\d", line)[0])})
    
  if k == 4:
    j = 2
    k = 0
    
# temporarily remove automata that are filed to compress.
for mnrl in failed_to_compress:
  pre_ste_dict.pop(mnrl, None)
  pre_fan_in_dict.pop(mnrl, None)
  pre_fan_out_dict.pop(mnrl, None)
  pre_node_degree_dict.pop(mnrl, None)
  compressability_dict.pop(mnrl, None)

# get the most frequent items from each dict
# returns (most_common_elements, occurrences)
#keys = Counter(pre_ste_dict.values())
#keys = Counter(post_ste_dict.values())
#keys = Counter(pre_fan_in_dict.values())
#keys = Counter(post_fan_in_dict.values())
#keys = Counter(pre_fan_out_dict.values())
#keys = Counter(post_fan_out_dict.values())
#keys = Counter(pre_node_degree_dict.values())
#keys = Counter(post_node_degree_dict.values())
keys = Counter(compressability_dict.values())
mode = keys.most_common(20)
print(mode)

# some histgrams.
#temp_1 = []
#temp_2 = []

# hist for STEs.
#for key, value in pre_ste_dict.items():
  #temp_1.append(value)
#for key, value in post_ste_dict.items():
  #temp_2.append(value)

# hist for fan-in.
#for key, value in pre_fan_in_dict.items():
  #temp_1.append(value)
#for key, value in post_fan_in_dict.items():
  #temp_2.append(value)
  
# hist for fan-out.
#for key, value in pre_fan_out_dict.items():
  #temp_1.append(value)
#for key, value in post_fan_out_dict.items():
  #temp_2.append(value)  

# hist for avg node degree
#for key, value in pre_node_degree_dict.items():
  #temp_1.append(value)
#for key, value in post_node_degree_dict.items():
  #temp_2.append(value)  
  

  
# hist for fan-out.
#for key, value in pre_fan_out_dict.items():
  #temp_1.append(value)
#for key, value in post_fan_out_dict.items():
  #temp_2.append(value)

# plot in log scale.
#plt.hist(temp_1, color='red', label='pre', alpha=0.5, histtype='step', log='true')
#plt.hist(temp_2, color='green', label='post', alpha=0.5, histtype='step', log='true')


#plt.hist([np.asarray(temp_1), np.asarray(temp_2)], color=['r','g'], alpha=0.8, label=['Pre Optimization','Post Optimization'], log=True)
#plt.title("STEs")
#plt.title("Fan-in")
#plt.title("Fan-out")
#plt.title("Avg Node Degree")

#plt.xlabel("Number of STEs")
#plt.xlabel("Number of Fan-in")
#plt.xlabel("Number of Fan-out")
#plt.xlabel("Average Node Degree")
#plt.ylabel("Number of automata")

#plt.legend(loc="upper right")
#plt.hist(np.asarray(temp_1))
#print(str(max(temp_1)))
#print(str(temp_1.count(6489)))

#plt.show()

# sort dicts on values on ascending order.
sorted_pre_ste_list = sorted(pre_ste_dict.items(), key=operator.itemgetter(1))
sorted_post_ste_list = sorted(post_ste_dict.items(), key=operator.itemgetter(1))

sorted_pre_fan_in_list = sorted(pre_fan_in_dict.items(), key=operator.itemgetter(1))
sorted_post_fan_in_list = sorted(post_fan_in_dict.items(), key=operator.itemgetter(1))

sorted_pre_fan_out_list = sorted(pre_fan_out_dict.items(), key=operator.itemgetter(1))
sorted_post_fan_out_list = sorted(post_fan_out_dict.items(), key=operator.itemgetter(1))

sorted_pre_fan_out_list = sorted(pre_fan_out_dict.items(), key=operator.itemgetter(1))
sorted_post_fan_out_list = sorted(post_fan_out_dict.items(), key=operator.itemgetter(1))

sorted_pre_node_degree_list = sorted(pre_node_degree_dict.items(), key=operator.itemgetter(1))
sorted_post_node_degree_list = sorted(post_node_degree_dict.items(), key=operator.itemgetter(1))

sorted_compressability_list = sorted(compressability_dict.items(), key=operator.itemgetter(1))


# print out the extremes.
#print("\n*** *** *** *** SNORT STATS *** *** *** ***\n")

#print("--- --- --- --- Snort STEs --- --- --- ---")
#print("Smallest pre-optimization STEs: " + str(sorted_pre_ste_list[0]))
#print("Largest pre-optimization STEs: " + str(sorted_pre_ste_list[len(sorted_pre_ste_list)-1]) + "\n")

#print("Smallest post-optimization STEs: " + str(sorted_post_ste_list[0]))
#print("Largest post-optimization STEs: " + str(sorted_post_ste_list[len(sorted_post_ste_list)-1]))

#print("")
#print("pre STEs: " + str(len(sorted_pre_ste_list)))
#print("post STEs: " + str(len(sorted_post_ste_list)))
#print("--- --- --- --- --- --- --- --- --- --- --- --- ---\n")

#print("\n--- --- --- --- Snort Fan-in --- --- --- ---")
#print("Smallest pre-optimization Fan-in: " + str(sorted_pre_fan_in_list[0]))
#print("Largest pre-optimization Fan-in: " + str(sorted_pre_fan_in_list[len(sorted_pre_fan_in_list)-1]) + "\n")

#print("Smallest post-optimization Fan-in: " + str(sorted_post_fan_in_list[0]))
#print("Largest post-optimization Fan-in: " + str(sorted_post_fan_in_list[len(sorted_post_fan_in_list)-1]))

#print("")
#print("pre Fan-in: " + str(len(sorted_pre_fan_in_list)))
#print("post Fan-in: " + str(len(sorted_post_fan_in_list)))
#print("--- --- --- --- --- --- --- --- --- --- --- --- ---\n")

#print("\n--- --- --- --- Snort Fan-out --- --- --- ---")
#print("Smallest pre-optimization Fan-out: " + str(sorted_pre_fan_out_list[0]))
#print("Largest pre-optimization Fan-out: " + str(sorted_pre_fan_out_list[len(sorted_pre_fan_out_list)-1]) + "\n")

#print("Smallest post-optimization Fan-out: " + str(sorted_post_fan_out_list[0]))
#print("Largest post-optimization Fan-out: " + str(sorted_post_fan_out_list[len(sorted_post_fan_out_list)-1]))

#print("")
#print("pre Fan-out: " + str(len(sorted_pre_fan_out_list)))
#print("post Fan-out: " + str(len(sorted_post_fan_out_list)))
#print("--- --- --- --- --- --- --- --- --- --- --- --- ---\n")

#print("\n--- --- --- --- Snort Average Node Degree --- --- --- ---")
#print("Smallest pre-optimization Avg node degree: " + str(sorted_pre_node_degree_list[0]))
#print("Largest pre-optimization Avg node degree: " + str(sorted_pre_node_degree_list[len(sorted_pre_node_degree_list)-1]) + "\n")

#print("Smallest post-optimization Avg node degree: " + str(sorted_post_node_degree_list[0]))
#print("Largest post-optimization Avg node degree: " + str(sorted_post_node_degree_list[len(sorted_post_node_degree_list)-1]))

#print("")
#print("pre avg node degree: " + str(len(sorted_pre_node_degree_list)))
#print("post avg node degree: " + str(len(sorted_post_node_degree_list)))
#print("--- --- --- --- --- --- --- --- --- --- --- --- ---\n")

#print("\n--- --- --- --- Snort Compressability --- --- --- ---")
#print("Smallest Compressability: " + str(sorted_compressability_list[0]))
#print("Largest Compressability: " + str(sorted_compressability_list[len(sorted_compressability_list)-1]))

#print("")
#print("pre compressability: " + str(len(sorted_pre_node_degree_list)))
#print("post compressability: " + str(len(sorted_post_node_degree_list)))
#print("--- --- --- --- --- --- --- --- --- --- --- --- ---\n")

#print("*** *** *** *** END STATS *** *** *** ***\n")
##print(sorted_pre_ste_list)


f.close()  

  