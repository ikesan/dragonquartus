from mergesort import *
from tohex import *
import sys,re

while True : 
    line = sys.stdin.readline()
    if not line : exit(0)
    for k,v in consts.items() :
        line = line.replace(k,"%s"%v)
    line = re.sub(r'\s*#.*','',line)    
    line = re.sub(r'.* global .*','',line)    
    for k,v in regVar.items() :
        line = line.replace(k,v)
    if line : 
        bin = getBin(line)
        print(line.replace("\n",""),end="")
        if bin != "### ERROR ###" : print("\t@ " + bin)
        else :print("")
