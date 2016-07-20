from shiftmif import *
import re
from pprint import pprint
from sortcode import code
#shift 0x200
#mem = [ 0,0,0,0, 0,0,0,0,   0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0,  0,0,0,0, 31,14,15,92, 65,35,89,79, 32,38,46,26, 43,38,32,79]
    
consts = {
    "SORT1_INDEX":'0x1',#0x1#テンポラリ領域(0x100)
    "SORT_LEN":   '0x4',#0x4#ソート長(0x400),
    "SORT2_INDEX":'0x6',#0x6#データ領域(0x600),
    "SORT_LI_SLL":'0x8',#0x8#0x400はliできないのでシフトする
    "NUM":     "0x0", # in memory(1,2:reserved)
    "FROM_MEM":"0x3", # in memory
    "TO_MEM":  "0x4", # in memory
    "TIMES":   "0x5", # in memory 
    "BEGIN":"0x6", #begin for debug(r1)
    "TOI":  "0x7", #toi   for debug(r2)
    "FLAG": "0x8", #flag  for debug(r3)
}

for k,v in consts.items() : exec(k + " = %s" % v)
#mem[0:4] = [n,i1,i2,fromMem,toMem] #(i1:1,i2:2でなければならない)
r0 = (0)  # r0 は0固定レジスタ
begin,toi,flag = (0,0,0)  
regVar = {"begin":"r1","toi":"r2","flag":"r3"} # レジスタのエイリアス
r4,r5,r6,r7 = (0,0,0,0)   # 
szcv = (0)
def setSZCV(expr):
    global szcv
    szcv = expr
def hlt():
    print(mem)
    print(cnt)
    exit(0)


def toAsms(code):
    asms = [] 
    labels = {} #label -> index
    for a in code.split("\n"):
        a = re.sub(r'#.+',"",a)
        a = a.replace('  ', "")
        if not a : continue
        if a.startswith('@') :
            labels[a] = len(asms)
        else :
            asms.append(a + "\n")    
    #set @
    for i,a in enumerate(asms):
        m = re.findall(r'(@[_a-zA-Z0-9]+)',a)
        if m :
            m = m[0]
            j = labels[m]-i
            assert(-0xff/2 <= j and j < 0xff/2)
            if j < 0 : j += 0xff
            else : j -= 0x01
            asms[i] = a.replace(m,str(hex(j)))
    return asms

def Hex(x):
    if x >= 0 and x <= 0x9: return x
    else : return hex(x)[2:]

if __name__ == "__main__" :
    asms = toAsms(code)
    print("".join(asms))
    mem = getMifArray(0x600)
    if any("-n" in s for s in sys.argv):exit(0)
    #asms = toAsms("b @a\nr4+=r4\nhlt()\n@a\nr4-=r4\nhlt()")#["b 0xff\n"]
    pc = 0
    cnt = 0
    while True :
        cnt += 1
        asm = asms[pc]
        #print([r4,r5,r6,r7,asm])
        #pprint([hex(pc),[Hex(x) for x in mem[0:8]],asm])
        #print([hex(pc),mem[0:9],asm])
        if asm.startswith("b ") :
            m = re.findall(r'b\s+0x([0-9a-f]{1,2})(?:\s+\?\s+(.+))?',asm)
            m = m[0]
            if (m[1]=='') or eval(m[1]):
                j = int(m[0],16)
                if j >= 0xff/2 : j -= 0xff + 1
                pc += j
        else :
            exec(asm)
        pc += 1
