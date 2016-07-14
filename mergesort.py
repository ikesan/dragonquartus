mem = [0,0,0,0,0,0,0,0, 31,14,15,92, 65,35,89,79, 32,38,46,26, 43,38,32,79, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
consts = {
    "SORT1_INDEX":"0x08",
    "SORT_LEN":   "0x10",
    "SORT2_INDEX":"0x18",
    "NUM":     "0x0", # in memory
    "FROM_MEM":"0x3", # in memory
    "TO_MEM":  "0x4", # in memory
}

for k,v in consts.items() : exec(k + " = %s" % v)
#mem[0:4] = [n,i1,i2,fromMem,toMem] #(i1:1,i2:2でなければならない)
r0 = 0  # r0 は0固定レジスタ
begin,toi,flag = 0,0,0  
regVar = {"begin":"r1","toi":"r2","flag":"r3"} # レジスタのエイリアス
r4,r5,r6,r7 = 0,0,0,0   # regester


def sort():
    global begin , toi , flag    
    global r0,r4,r5,r6,r7
    global mem
    begin = 0 
    while begin - SORT_LEN < 0:
        mem[r0+0x01] = begin #i1   
        r4 = mem[r0+NUM]     #i2
        r4 += begin          # :
        mem[r0+0x02] = r4    # :
        toi = begin
        flag = 0 
        while flag - 3 != 0:
            # r7 required in this block
            if flag - 2 == 0 :
                r7 = 1
            else :
                if flag - 1 == 0 :
                    r7 = 2
                else :
                    r4 = mem[r0+FROM_MEM] # mem[mem[FROM_MEM] + mem[1]] - mem[mem[FROM_MEM]+mem[2]]
                    r6 = mem[r0+0x01]
                    r6 += r4 
                    r6 = mem[r6+0x00]
                    r5 = mem[r0+0x02]
                    r5 += r4 
                    r5 = mem[r5+0x00]
                    if r6 - r5 < 0 :
                        r7 = 0x01
                    else :
                        r7 = 0x02
            r4 = mem[r0+FROM_MEM] # mem[mem[toMem] + toi] = mem[mem[FROM_MEM]+mem[r7]]
            r5 = mem[r7+0x00]        # :
            r4 += r5              # :
            r4 = mem[r4+0x00]        # :
            r5 = mem[r0+TO_MEM]   # :
            r5 += toi             # :
            mem[r5+0x00] = r4        # :
            r4 = mem[r7+0x00] #i +=1
            r4 += 1        # :
            mem[r7+0x00] = r4 # :
            r5 = mem[r0+NUM] # if i >= begin + i * n : flag += i
            if r7 - 2 == 0 :
                r5 += r5    # r4 overlap(mem[r7])
            r5 += begin
            if r4 - r5 >= 0 :
                flag += r7
            toi += 1
        r4 = mem[r0+NUM]  # begin += n * 2
        r4 += r4        # :
        begin += r4     # :


if __name__ == "__main__" :
    # while r0 - r1 == 0:  => cmp r0 r1 ; bne <>
    # if r0 - r1 == 0   :  => cmp r0 r1 ; bne <elseの先>
    print(mem)

    r4 = 0x01
    mem[r0+NUM] = r4
    r4 = SORT1_INDEX
    mem[r0+FROM_MEM] = r4
    r4 =  SORT2_INDEX
    mem[r0+TO_MEM] = r4
    sort()
    print(mem)

    r4 = 0x02
    mem[r0+NUM] = r4
    r4 = SORT1_INDEX
    mem[r0+TO_MEM] = r4
    r4 =  SORT2_INDEX
    mem[r0+FROM_MEM] = r4
    sort()
    print(mem)

    r4 = 0x04
    mem[r0+NUM] = r4
    r4 = SORT1_INDEX
    mem[r0+FROM_MEM] = r4
    r4 =  SORT2_INDEX
    mem[r0+TO_MEM] = r4
    sort()
    print(mem)

    r4 = 0x08
    mem[r0+NUM] = r4
    r4 = SORT1_INDEX
    mem[r0+TO_MEM] = r4
    r4 =  SORT2_INDEX
    mem[r0+FROM_MEM] = r4
    sort()
    print(mem)
