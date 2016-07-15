code = """
@mergesort
    mem[r0+NUM] = 0x01
    mem[r0+TIMES] = 0x0a #0x04
    r4 = SORT2_INDEX
    r4 <<= SORT_LI_SLL
    mem[r0+FROM_INDEX] = r4
    r4 = SORT1_INDEX
    r4 <<= SORT_LI_SLL
    mem[r0+TO_INDEX]   = r4  
    r4 = mem[r0+TIMES] 
    @while0
    setSZCV( r4 - 0)
    b @while1 ? szcv <= 0  
        r4 = mem[r0+FROM_INDEX]
        mem[r0+FROM_MEM] = r4
        r4 = mem[r0+TO_INDEX] 
        mem[r0+TO_MEM] = r4
        b @sort
        @sortend
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
        b @while0
    @while1
    hlt()
@sort
    begin = 0 
    r4 = SORT_LEN
    r4 <<= SORT_LI_SLL    
    @while2
    setSZCV(begin - r4)
    b @sortend ? szcv >= 0  # b - r4 >= 0 <=> -b + r4 <= 0
        mem[r0+0x01] = begin #i1 = begin 
        r4 = mem[r0+NUM]     #i2 = begin + n
        r4 += begin          # :
        mem[r0+0x02] = r4    # :
        toi = begin
        flag = 0 
        @while4
        setSZCV(flag - 3)
        b @while5 ? szcv == 0 # r7 reserved in this block 
            setSZCV(flag - 2)
            b @if0 ? szcv != 0 
                r7 = 1
                b @if1
            @if0
                setSZCV(flag - 1)
                b @if2 ? szcv != 0
                    r7 = 2
                    b @if3
                @if2
                    r4 = mem[r0+FROM_MEM] # mem[mem[FROM_MEM] + mem[1]] - mem[mem[FROM_MEM]+mem[2]]
                    r6 = mem[r0+0x01]     # : mem[mem[from] + i1] - mem[mem[from] + i2]
                    r6 += r4 
                    r6 = mem[r6+0x00]
                    r5 = mem[r0+0x02]
                    r5 += r4 
                    r5 = mem[r5+0x00]
                    setSZCV(r6 - r5)
                    b @if4 ? szcv < 0 
                        r7 = 0x02
                        b @if5
                    @if4
                        r7 = 0x01
                    @if5
                @if3
            @if1
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
            b @ifA ? szcv != 0
                r5 += r5    # r4 overlap(mem[r7])
            @ifA
            r5 += begin
            setSZCV(r4 - r5)            
            b @ifB ? szcv < 0
                flag += r7
            @ifB
            toi += 1
            b @while4
        @while5
        r4 = mem[r0+NUM]  # begin += n * 2
        r4 += r4        # :
        begin += r4     # :
        r4 = SORT_LEN
        r4 <<= SORT_LI_SLL    
        b @while2
"""
