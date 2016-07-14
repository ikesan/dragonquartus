from shiftmif import *
#mem = [0,0,0,0,0,0,0,0, 31,14,15,92, 65,35,89,79, 32,38,46,26, 43,38,32,79, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
#shift 0x200

consts = {
    "SORT1_INDEX":'0x1',#テンポラリ領域(0x100)
    "SORT_LEN":   '0x4',#ソート長(0x400),
    "SORT2_INDEX":'0x6',#データ領域(0x600),
    "SORT_LI_SLL":'0x8', #0x400はliできないのでシフトする
    "NUM":     "0x0", # in memory
    "FROM_MEM":"0x3", # in memory
    "TO_MEM":  "0x4", # in memory
    "TIMES": "0x5",
    "FROM_INDEX":"0x6",#
    "TO_INDEX":"0x7",#
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

def mergesort():
    global mem,r4,r5,szcv
    mem = getMifArray(0x600)
    # while r0 - r1 == 0:  => cmp r0 r1 ; bne <>
    # if r0 - r1 == 0   :  => cmp r0 r1 ; bne <elseの先>
    #0x200
    mem[r0+NUM] = 0x01
    mem[r0+TIMES] = 0x0a
    r4 = SORT2_INDEX
    r4 <<= SORT_LI_SLL
    mem[r0+FROM_INDEX] = r4
    r4 = SORT1_INDEX
    r4 <<= SORT_LI_SLL
    mem[r0+TO_INDEX]   = r4  
    r4 = mem[r0+TIMES] 
    setSZCV( r4 - 0)
    while szcv > 0 :
        r4 = mem[r0+FROM_INDEX]
        mem[r0+FROM_MEM] = r4
        r4 = mem[r0+TO_INDEX] 
        mem[r0+TO_MEM] = r4
        sort()
        r5 = mem[r0+FROM_INDEX]
        r4 = mem[r0+TO_INDEX]
        mem[r0+FROM_INDEX] = r4
        mem[r0+TO_INDEX] = r5
        r4 = mem[r0+NUM] 
        r4 += r4
        mem[r0+NUM] = r4
        r4 = mem[r0+TIMES]
        r4 -= 1
        mem[r0+TIMES] = r4
        setSZCV( r4 - 0)


def sort():
    global begin , toi , flag    
    global r0,r4,r5,r6,r7
    global mem,szcv
    begin = 0 
    r4 = SORT_LEN
    r4 <<= SORT_LI_SLL    
    setSZCV(begin - r4)
    while szcv < 0:
        mem[r0+0x01] = begin #i1 = begin 
        r4 = mem[r0+NUM]     #i2 = begin + n
        r4 += begin          # :
        mem[r0+0x02] = r4    # :
        toi = begin
        flag = 0 
        setSZCV(flag - 3)
        while szcv != 0: # r7 reserved in this block 
            setSZCV(flag - 2)
            if szcv == 0 :
                r7 = 1
            else :
                setSZCV(flag - 1)
                if szcv == 0 :
                    r7 = 2
                else :
                    r4 = mem[r0+FROM_MEM] # mem[mem[FROM_MEM] + mem[1]] - mem[mem[FROM_MEM]+mem[2]]
                    r6 = mem[r0+0x01]     # : mem[mem[from] + i1] - mem[mem[from] + i2]
                    r6 += r4 
                    r6 = mem[r6+0x00]
                    r5 = mem[r0+0x02]
                    r5 += r4 
                    r5 = mem[r5+0x00]
                    setSZCV(r6 - r5)
                    if szcv < 0 :
                        r7 = 0x01
                    else :
                        r7 = 0x02
            r4 = mem[r0+FROM_MEM] # mem[mem[toMem] + toi] = mem[mem[FROM_MEM]+mem[r7]]
            r5 = mem[r7+0x00]     # :
            r4 += r5              # :
            r4 = mem[r4+0x00]     # :
            r5 = mem[r0+TO_MEM]   # :
            r5 += toi             # :
            mem[r5+0x00] = r4     # :
            r4 = mem[r7+0x00] #i +=1
            r4 += 1           # :
            mem[r7+0x00] = r4 # :
            r5 = mem[r0+NUM] # if i >= begin + i * n : flag += i
            setSZCV(r7 - 2)
            if szcv == 0 :
                r5 += r5    # r4 overlap(mem[r7])
            r5 += begin
            setSZCV(r4 - r5)            
            if szcv >= 0 :
                flag += r7
            toi += 1
            setSZCV(flag - 3)
        r4 = mem[r0+NUM]  # begin += n * 2
        r4 += r4        # :
        begin += r4     # :
        r4 = SORT_LEN
        r4 <<= SORT_LI_SLL    
        setSZCV(begin - r4)


if __name__ == "__main__" :
    mergesort()
    print(mem)
