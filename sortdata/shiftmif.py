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

def shiftcmds(shift = 0x100):    
    while True : 
        line = sys.stdin.readline()
        if not line : return 
        m = re.findall(r'(\s+)(.+?)(\s+):(.+?);',line)
        if m :
            m = m[0]
            print(m[0] + findandAdd(m[1],shift) + m[2] + ":" + m[3] + ";")
        else : 
            m = re.findall(r'DEPTH=(\d+);',line)
            if m :
                m = m[0]
                added = str(int(m) + shift)
                line = line.replace(m,added) 
            print(line.strip("\n"))

def getMifArray(startIndex = 0x500):
    arr = []
    while True : 
        line = sys.stdin.readline()
        if not line : 
            th = [0] * startIndex            
            return th + arr
        m = re.findall(r'(\s+)(.+?)(\s+):(.+?);',line)
        if m :
            m = m[0]
            try :
                arr.append( int(m[3]))
            except : pass            
    
def makeMif(arr):
    res = ""
    contents = [
        "WIDTH=16;",
        "DEPTH="+str(len(arr))+";",
        "ADDRESS_RADIX=DEC;",
        "DATA_RADIX=DEC;",
        "CONTENT BEGIN",
    ]    
    for c in contents : res += c + "\n"
    for i,a in enumerate(arr) :
        res += "  " + str(i) + " : " + str(a) + ";\n" 
    return res + "END;"

if __name__ == "__main__" :
    arr = getMifArray()
    print(arr)
    print(len(arr))