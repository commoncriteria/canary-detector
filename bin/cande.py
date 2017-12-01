#!/usr/bin/env python3
import subprocess
import re
import sys



######
def analyze(filepath, is_concise):
  # Objdump
  proc = subprocess.Popen('objdump -M intel -d ' + filepath, shell=True, stdout=subprocess.PIPE)

  # This is the regex for gcc-compiled stack canaries
  regstackfail = re.compile('.*__stack_chk_fail.*');

  # Sequence of regexs for windows-compiled stack canaries
  regexs=[ re.compile('^mov\s+rcx\,QWORD\ PTR\ \[rsp'),
           re.compile('^xor\s+rcx'),
           re.compile('^call') ]

  # Tracks the number of lines matched
  linesmatched=0
  for byteline in proc.stdout:
    # Convert bytestream to string
    line = byteline.decode("utf-8")

    # If we found the line
    if regstackfail.match(line):
      # Quit happily
      print("Found gcc-style canary in '" + filepath+ "' " + line.split('\t')[0]);
      if is_concise:
        return

    # Split on tabs
    instr = line.split('\t')
    if len(instr) == 3:
      # If we match the current one
      if regexs[ linesmatched ].match(instr[2]):
        # Increment the matched counter
        linesmatched+=1
        # If there are no more lines to match
        if linesmatched==len(regexs):
          print("Found ms-style canary in '" + filepath + "' " + instr[0])
          # Reset counter
          linesmatched=0
          if is_concise:
            return
          
      else:
        linesmatched=0
#######          

 

if len(sys.argv) == 1:
  print( "Usage: cande.py [-v] [<file-1> [ ...]]")
  sys.exit(0)

execname=""  
try:
  subprocess.Popen('objdump -v', shell=True)
  execname="objdump"
except:
  # 
  # try:
  #   subprocess.Popen('dumpbin')
  #   execname="dumpbin"
  # except:
  #   print("This utility relies on either dumpbin(on Microsoft Windows) or objdump(on other OSs)")
  print("This utility relies on objdump (a basic GNU utility). Please ensure that it is installed and included in your path.")
  sys.exit(1)
    
is_concise=True
for ii in range(1, len(sys.argv)):
  if sys.argv[ii]=='-q':
    is_concise=True
  elif sys.argv[ii]=='-v':
    is_concise=False
  else:
    analyze(sys.argv[ii], is_concise)
