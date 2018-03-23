# Snort_Generation
A repository dedicated to generate and characterize automata from Snort rulesets PCREs. It needs [this version of hscompile](https://github.com/LingxiWu/hscompile.git) for some of the tasks. A detailed instructions on the usages and installation of hscompile is [here](https://github.com/kevinaangstadt/hscompile.git)

## From PCREs to Automaton
To ganerate .mnrl file run the following steps in order. Pay close attention to the input and output of each step.<br/>
**Step - 1: run *select_pcre.py***

Description:<br />
A simple python script which traverses through all Snort rule files to extract PCREs. It does NOT filter out illegal PCREs.
  
Path:<br />
/scripts/select_pcre.py
  
Input:<br/>
Snort Ruleset files path
  
Output:<br />
It generates a .regex file which contains all Snort PCREs (including duplicates)
  
Sample Usage:<br/>
```python select_pcre.py --rules_path="/path/to/all/Snort/ruleset/files/" --regex_fn="/path/to/extracted/PCREs/snort.regex"```

**Step - 2: run *regex_filter***

Description:<br />
It filters out duplicates and illegal PCREs, and log error messages. However, it does NOT deal with modifiers.
  
Path:<br />
Source file: /hscompile/src/regex_filter.cpp
  
Input:<br/>
Path to .regex file containing all Snort PCREs from step-1
  
Output:<br />
A regex file which has legal PCREs from Snort without duplicates
  
Sample Usage:<br/>
```./regex_filter <snort_regex_file_name> <filtered_snort_regex_file_path>```


**Step - 3: run *pcre2mnrl***

Description:<br />
Generate automaton from a regex file. Usage: ./pcre2mnrl [FLAG] <regex_file_path> <mnrl_file_path>". [FLAG] is optional. By deafult, pcre2mnrl supports backwards compatibility. -f, --force 	Force compilation by discarding invalid modifiers.
  
Path:<br />
Source file: /hscompile/src/pcre2mnrl.cpp
  
Input:<br/>
Path to .regex file containing all Snort PCREs from step-2
  
Output:<br />
An automaton description in .mnrl file.
  
Sample Usage:<br/>
```./pcre2mnrl <regex_file_path> <mnrl_file_path>```<br /> 
or<br/>
```./pcre2mnrl -f <regex_file_path> <mnrl_file_path> ```
