



"""
mem = [0,0,0,0, 31,14,15,92, 65,35,89,79, 32,38,46,26, 43,38,32,79, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]

def ld(rb,d): global mem ; return mem[rb + d]
def st(rb,d,ra) : global mem ; mem[rb + d] = ra    
def ldMem(d): global mem ; return mem[d]
def stMem(d,ra): global mem ; mem[d] = ra
#const
sort1Index = 4
sortLen = 16
sort2Index = sort1Index + sortLen
#r0 = 0
#r1 = begin
#r2 = toi
#mem[0:4] = [n,i1,i2,fromMem,toMem]

def sort(n,fromMem,toMem):
    begin = 0 
    while begin < sortLen :
        i1 ,i2 = begin ,begin + n
        toi = begin
        flag = 0 # f2,f1
        while flag != 3:
            if flag == 2 or (flag == 0 and ld(fromMem,i1) < ld(fromMem,i2)) :  
                st(toMem,toi,ld(fromMem,i1)) 
                i1 += 1
                if i1 >= begin + 1 * n : flag += 1
            else :
                st(toMem,toi,ld(fromMem,i2)) 
                i2 += 1
                if i2 >= begin + 2 * n : flag += 2
            toi += 1
        begin += 2 * n

print(mem)
sort(1,sort1Index,sort2Index)
print(mem)
sort(2,sort2Index,sort1Index)
print(mem)
sort(4,sort1Index,sort2Index)
print(mem)
sort(8,sort2Index,sort1Index)
print(mem)


"""

"""
mem1 = [31,14,15,92, 65,35,89,79, 32,38,46,26, 43,38,32,79]
mem2 = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
def sort(n,fromMem,toMem):
    def sortRegion(begin):
        i1 ,i2 = begin ,begin + n
        e1 ,e2 = i2,i2 + n
        f1 ,f2 = False ,False    
        toi = begin
        while True:
            if f1 and f2 : return 
            if f2 or ((not f1) and fromMem[i1] < fromMem[i2]) :  
                toMem[toi] = fromMem[i1]
                toi += 1
                i1 += 1
                if i1 >= e1 : f1 = True
            else :
                toMem[toi] = fromMem[i2]
                toi += 1
                i2 += 1
                if i2 >= e2 : f2= True
    i = 0 
    while True :
        sortRegion(i)
        i += 2 * n
        if i >= len(fromMem) : return 

print((mem1,mem2))
sort(1,mem1,mem2)
print((mem1,mem2))
sort(2,mem2,mem1)
print((mem1,mem2))
sort(4,mem1,mem2)
print((mem1,mem2))
sort(8,mem2,mem1)
print((mem1,mem2))

"""


"""
mem = [31,14,15,92, 65,35,89,79, 32,38,46,26, 43,38,32,79]
def sort(n):
    global mem
    def sortRegion(begin):
        i1 ,i2 = begin ,begin + n
        e1 ,e2 = i2,i2 + n
        f1 ,f2 = False ,False    
        res = []
        while True:
            if f1 and f2 : return res
            if f2 or ((not f1) and mem[i1] < mem[i2]) :  
                res.append(mem[i1])
                i1 += 1
                if i1 >= e1 : f1 = True
            else :
                res.append(mem[i2])
                i2 += 1
                if i2 >= e2 : f2= True
        return res
    i ,res = 0 ,[]    
    while True :
        res.extend(sortRegion(i))
        i += 2 * n
        if i >= len(mem) : 
            mem = res
            return 
            
print(mem)
sort(1)
print(mem)
sort(2)
print(mem)
sort(4)
print(mem)
sort(8)
print(mem)
"""