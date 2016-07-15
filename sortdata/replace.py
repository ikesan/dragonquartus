from mergesort import *
from tohex import *
from fromhex import * 
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
        code ,cmd = "",""
        if not any("-n" in s for s in sys.argv):
            code = " | " + line.replace("\n","")
        if bin != "### ERROR ###" : 
            if not any("-c" in s for s in sys.argv):
                cmd = " | " + getCmd(bin)
            print(bin + cmd + code)
        else :
            if code : print("    " + code)