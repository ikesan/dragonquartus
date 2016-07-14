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
        if len(sys.argv) > 1 and sys.argv[1] == "-n" : 
            code = ""
        else : code = " |" + line.replace("\n","")
        if bin != "### ERROR ###" : 
            print(bin + code)
        else :
            if code : print("    " + code)
