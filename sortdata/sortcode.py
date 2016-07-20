code = """
@mergesort
    r4 = 0x01  # FOR DEBUG は消して良い / FOR FIX は修正したもの
    mem[r0+NUM] = r4
    r4 = 0x0a #0x04
    mem[r0+TIMES] = r4
    r4 = SORT2_INDEX
    r4 <<= SORT_LI_SLL
    mem[r0+FROM_MEM] = r4
    r4 = SORT1_INDEX
    r4 <<= SORT_LI_SLL
    mem[r0+TO_MEM] = r4  
    b @checkOrdered
    @checkOrderedEnd
    b @checkROrdered
    @checkROrderedEnd
    r4 = mem[r0+TIMES] 
    @while0
    setSZCV( r4 - 0)
    b @while1 ? szcv <= 0  
        b @sort
        @sortend
        r5 = mem[r0+FROM_MEM]
        r4 = mem[r0+TO_MEM]
        mem[r0+FROM_MEM] = r4
        mem[r0+TO_MEM] = r5
        r4 = mem[r0+NUM] 
        r4 += r4
        mem[r0+NUM] = r4
        r4 = mem[r0+TIMES]
        r4 -= 1
        mem[r0+TIMES] = r4
        b @while0
    @while1
    hlt()
@checkOrdered
    r4 = SORT_LEN
    r4 <<= SORT_LI_SLL    #r4:1024    
    r7 = mem[r0+FROM_MEM] #r7:from_mem
    @cowhile
    r4 -= 1
    setSZCV(r4-0)
    b @cofinished ? szcv == 0
        r5 = mem[r7+0]
        r6 = mem[r7+1]
        setSZCV(r6 - r5)
        b @checkOrderedEnd ? szcv < 0
        r7 += 1
        b @cowhile
    @cofinished
    hlt()
@checkROrdered
    r4 = SORT_LEN
    r4 <<= SORT_LI_SLL    #r4:1024    
    r7 = mem[r0+FROM_MEM] #r7:from_mem
    @corwhile
    r4 -= 1
    setSZCV(r4-0)
    b @reverseROrdered ? szcv == 0
        r5 = mem[r7+0]
        r6 = mem[r7+1]
        setSZCV(r5 - r6)
        b @checkROrderedEnd ? szcv < 0
        r7 += 1
        b @corwhile
@reverseROrdered
    r4 = mem[r0+FROM_MEM]
    r5 = SORT_LEN
    r5 <<= SORT_LI_SLL
    r5 += r4
    r5 -= 1
    @rrowhile
    setSZCV(r5-r4)
    b @rrofinished ? szcv <= 0
        r6 = mem[r4+0]
        r7 = mem[r5+0]
        mem[r4+0] = r7
        mem[r5+0] = r6
        r4 += 1
        r5 -= 1
        b @rrowhile
    @rrofinished
    hlt()
@sort
    begin = 0 
    @while2
    r4 = SORT_LEN
    r4 <<= SORT_LI_SLL    
    setSZCV(r4 - begin)
    b @sortend ? szcv <= 0  # b - r4 >= 0 <=> -b + r4 <= 0
        mem[r0+0x01] = begin #i1 = begin 
        r4 = mem[r0+NUM]     #i2 = begin + n
        r4 += begin          # :
        mem[r0+0x02] = r4    # :
        toi = mem[r0+0x01]   # FOR FIX (before : begin) mov命令がバグ
        flag = 0 
        @while4
        # mem[r0+BEGIN] = begin # FOR DEBUG
        # mem[r0+TOI]   = toi   # FOR DEBUG
        # mem[r0+FLAG]  = flag  # FOR DEBUG (1->2->8... -> Flagが毎回更新されて3になってジャンプ)
        setSZCV(flag - 3)     # cmp命令が怪しい ? 
        b @while5 ? szcv == 0 # r7 reserved in this block (取ってくる方)
            setSZCV(flag - 2) # 一つ一つについて
            b @if0 ? szcv != 0 
                r7 = 1   # flag == 2 => r7 = 1
                b @if1
            @if0
                setSZCV(flag - 1)
                b @if2 ? szcv != 0
                    r7 = 2  # flag == 1 => r7 = 2
                    b @if3
                @if2
                    r4 = mem[r0+FROM_MEM] # mem[mem[FROM_MEM] + mem[1]] - mem[mem[FROM_MEM]+mem[2]]
                    r6 = mem[r0+0x01]     # : mem[mem[from] + i1] - mem[mem[from] + i2]
                    r6 += r4              # : flag == 0 => r7 = 小さい方
                    r6 = mem[r6+0x00]
                    r5 = mem[r0+0x02]
                    r5 += r4 
                    r5 = mem[r5+0x00]
                    setSZCV(r6 - r5)
                    b @if4 ? szcv < 0 
                        r7 = 0x02
                        b @if5
                    @if4
                        r7 = 0x01   # 8701 => 
                    @if5
                @if3
            @if1
            r4 = mem[r0+FROM_MEM] # mem[mem[toMem] + toi] = mem[mem[FROM_MEM]+mem[r7]]
            r5 = mem[r7+0x00]     # :toiのところに書き込み
            r4 += r5              # :
            r4 = mem[r4+0x00]     # :
            r5 = mem[r0+TO_MEM]   # :
            r5 += toi             # :
            mem[r5+0x00] = r4     # :
            r4 = mem[r7+0x00] # m[r7] +=1
            r4 += 1           # :
            mem[r7+0x00] = r4 # :
            r5 = mem[r0+NUM]    # if m[r7] >= begin + r7 * n : flag += r7
            setSZCV(r7 - 2)     # 
            b @ifA ? szcv != 0
                r5 += r5    # r4 overlap(mem[r7])
            @ifA
            r5 += begin
            # mem[r0+0xb] = r4 # FOR DEBUG
            # mem[r0+0xc] = r5 # FOR DEBUG
            setSZCV(r4 - r5) # (s,vがおかしい(s^vをsにしたら程よくなった)))
            b @ifB ? szcv < 0  # <=系 は zeroの条件で成立なので大丈夫だった
                flag += r7
            @ifB
            toi += 1
            # mem[r0+FLAG]  = flag  # FOR DEBUG 
            b @while4
        @while5
        r4 = mem[r0+NUM]  # begin += n * 2
        r4 += r4        # :
        begin += r4     # :
        b @while2
"""


oldcode = """
@mergesort
    r4 = 0x01
    mem[r0+NUM] = r4
    r4 = 0x0a #0x04
    mem[r0+TIMES] = r4
    r4 = SORT2_INDEX
    r4 <<= SORT_LI_SLL
    mem[r0+FROM_MEM] = r4
    r4 = SORT1_INDEX
    r4 <<= SORT_LI_SLL
    mem[r0+TO_MEM] = r4  
    r4 = mem[r0+TIMES] 
    @while0
    setSZCV( r4 - 0)
    b @while1 ? szcv <= 0  
        b @sort
        @sortend
        r5 = mem[r0+FROM_MEM]
        r4 = mem[r0+TO_MEM]
        mem[r0+FROM_MEM] = r4
        mem[r0+TO_MEM] = r5
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
    @while2
    r4 = SORT_LEN
    r4 <<= SORT_LI_SLL    
    setSZCV(r4 - begin)
    b @sortend ? szcv <= 0  # b - r4 >= 0 <=> -b + r4 <= 0
        mem[r0+0x01] = begin #i1 = begin 
        r4 = mem[r0+NUM]     #i2 = begin + n
        r4 += begin          # :
        mem[r0+0x02] = r4    # :
        toi = begin
        flag = 0 
        @while4
        # mem[r0+BEGIN] = begin # FOR DEBUG
        # mem[r0+TOI]   = toi   # FOR DEBUG
        # mem[r0+FLAG]  = flag  # FOR DEBUG
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
        b @while2
"""
