from shiftmif import *
import sys,re
lines = []
while True : 
    line = sys.stdin.readline()
    if not line : 
        print(makeMif(lines))
        exit(0)
    else :
        lines.append(line.replace("\n",""))
    