def qsort(l,r):
    if l < r :
        i,j = l,r
        p = mem[i]
        while True :
            while mem[i] < p : i += 1
            while mem[j] > p : j -= 1
            if i >= j : break
            mem[i],mem[j] = mem[j],mem[i]
            i += 1
            j -= 1
        qsort(l,i-1)
        qsort(j+1,r)
def med(x,y,z):
    if x < y :
        if y < z : return y
        if z < x : return x
        return z
    if x < z : return x
    if y < z : return y
    return z


code = """  # r1:left,r2:right,r6:jump,r7:top | r3:i,r4:j,r5:piv
@main        
    r1 = SORT2_INDEX
    r1 <<= SORT_LI_SLL    
    r2 = SORT_LEN
    r2 <<= SORT_LI_SLL
    r2 += r1
    r2 -= 1
    r6 = 0
    r7 = 0x10
    b @quicksort
    hlt()
@piv    #r3,r4,r5 -> r5
    setSZCV(r3-r4)
    b @pivend ? szcv < 0
    setSZCV(r5-r3) 
    b @pivif2 ? szcv < 0
        r5 = r3
        b @pivend
    @pivif2
    setSZCV(r5-r4)
    b @pivend ? szcv < 0
        r5 = r4
        b @pivend
    hlt()
@quicksort
    setSZCV( r2 - r1 )
    b @qrrif ? szcv <= 0
        r3 = mem[r1+0]
        r4 = mem[r2+0]
        r5 = r2
        r5 -= r1
        r5 >>= 1
        r5 += r1
        r5 = mem[r5+0]
        b @piv        
        @pivend
        mem[r0+1] = r1
        mem[r0+2] = r2
        r3 = r1
        r4 = r2
        @qwhile
            @qw1  
            r1 = mem[r3+0]
            setSZCV(r1-r5)     
            b @qwf1 ? szcv >= 0
                r3 += 1
                b @qw1
            @qwf1
            @qw2
            r1 = mem[r4+0]
            setSZCV(r5-r1)
            b @qwf2 ? szcv >= 0
                r4 -= 1
                b @qw2
            @qwf2
            setSZCV(r4-r3)
            b @qwhileend ? szcv <= 0
            r1 = mem[r3+0]
            r2 = mem[r4+0]
            mem[r3+0] = r2
            mem[r4+0] = r1
            r3 += 1
            r4 -= 1
            b @qwhile
        @qwhileend
        r1 = mem[r0+1]
        r2 = mem[r0+2]
        mem[r7+0] = r4+1 #s-q2right
        mem[r7+1] = r2  #s-q2left
        mem[r7+2] = r6  #s-jump
        r1 = r1        #q1:
        r2 = r3        #  :
        r2 -= 1
        r6 = 1         #  :
        r7 += 3        
        b @quicksort
        @q1end
        r7 -= 3
        r1 = mem[r7+0] #  :
        r2 = mem[r7+1] #  :
        r6 = 2         #  :
        r7 += 3        
        b @quicksort
        @q2end
        r7 -= 3
        r6 = mem[r7+2]
    @qrrif        
    setSZCV(r6-1)
    b @q1end ? szcv == 0
    setSZCV(r6-2)
    b @q2end ? szcv == 0
    hlt()    
"""

codew = """
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
