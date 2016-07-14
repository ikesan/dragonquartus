import sys,re

def add (s,d):
    s = "0x" + s
    s = int(s,16)
    s += d
    s = hex(s)
    return s.replace('0x','')
    
def findandAdd(s,d):
    match = re.findall(r'[0-9a-f]+',s)
    for m in match:
        if m == '000' : continue
        added = add(m,d)
        s = s.replace(m,added)
    return s


while True : 
    line = sys.stdin.readline()
    if not line : exit(0)
    m = re.findall(r'(\s+)(.+?)(\s+):(.+?);',line)
    if m :
        m = m[0]
        print(m[0] + findandAdd(m[1],0x100) + m[2] + ":" + m[3] + ";")
    else : print(line.strip("\n"))
