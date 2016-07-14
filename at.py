mem = [0,0,0,0,0,0,0,0, 31,14,15,92, 65,35,89,79, 32,38,46,26, 43,38,32,79, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
consts = {
    "8":0x08,
    "16":   0x10,
    "24":0x08+0x10,
    "0":       0,
    "3":0x3,
    "4":  0x4,
}
for k,v in consts.items() : exec(k + " = %s" % v)

r0 = 0	@ 8000
r1,r2,r3 = 0,0,0  	@ 8300
regVar = {"r1":"r1","r2":"r2","r3":"r3"}
r4,r5,r6,r7 = 0,0,0,0	@ 8700

def sort():



    r1 = 0 	@ 8100
    while r1 - 16 < 0:	@ 9916
        mem[r0+1] = r1	@ 4801
        r4 = mem[r0+0]	@ 2000
        r4 += r1	@ cc00
        mem[r0+2] = r4	@ 6002
        r2 = r1	@ ca60
        r3 = 0 	@ 8300
        while r3 - 3 != 0:	@ 9b03

            if r3 - 2 == 0 :	@ 9b02
                r7 = 1	@ 8701
            else :
                if r3 - 1 == 0 :	@ 9b01
                    r7 = 2	@ 8702
                else :
                    r4 = mem[r0+3]	@ 2003
                    r6 = mem[r0+1]	@ 3001
                    r6 += r4 	@ e600
                    r6 = mem[r6+0]	@ 3600
                    r5 = mem[r0+2]	@ 2802
                    r5 += r4 	@ e500
                    r5 = mem[r5+0]	@ 2d00
                    if r6 - r5 < 0 :	@ ee50
                        r7 = 1	@ 8701
                    else :
                        r7 = 2	@ 8702
            r4 = mem[r0+3]	@ 2003
            r5 = mem[r7+0]	@ 2f00
            r4 += r5	@ ec00
            r4 = mem[r4+0]	@ 2400
            r5 = mem[r0+4]	@ 2804
            r5 += r2	@ d500
            mem[r5+0] = r4	@ 6500
            r4 = mem[r7+0]	@ 2700
            r4 += 1	@ 8c01
            mem[r7+0] = r4	@ 6700
            r5 = mem[r0+0]	@ 2800
            if r7 - 2 == 0 :	@ 9f02
                r5 += r5	@ ed00
            r5 += r1	@ cd00
            if r4 - r5 >= 0 :	@ ec50
                r3 += r7	@ fb00
            r2 += 1	@ 8a01
        r4 = mem[r0+0]	@ 2000
        r4 += r4	@ e400
        r1 += r4	@ e100


if __name__ == "__main__" :


    print(mem)

    mem[r0+0] = 0x01	@ 4000
    mem[r0+3] = 8
    mem[r0+4] = 24	@ 5004
    sort()
    print(mem)

    mem[r0+0] = 0x02	@ 4000
    mem[r0+4] = 8
    mem[r0+3] = 24	@ 5003
    sort()
    print(mem)

    mem[r0+0] = 0x04	@ 4000
    mem[r0+3] = 8
    mem[r0+4] = 24	@ 5004
    sort()
    print(mem)

    mem[r0+0] = 0x02	@ 4000
    mem[r0+4] = 8
    mem[r0+3] = 24	@ 5003
    sort()
    print(mem)
