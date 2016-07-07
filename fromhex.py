import sys,re
if __name__ != "__main__" : exit(0)
    
def tobin16(line):
    bindic = {
        "0":"0000", "1":"0001", "2":"0010", "3":"0011" ,
        "4":"0100", "5":"0101", "6":"0110", "7":"0111" ,
        "8":"1000", "9":"1001", "a":"1010", "b":"1011" ,
        "c":"1100", "d":"1101", "e":"1110", "f":"1111" ,
    }
    return bindic[line[0]] + bindic[line[1]] + bindic[line[2]] + bindic[line[3]]

bin3toNum = {
    "000":"0","001":"1","010":"2","011":"3",
    "100":"4","101":"5","110":"6","111":"7"
}

bin4toNum = {
    "0000":"0","0001":"1","0010":"2","0011":"3",
    "0100":"4","0101":"5","0110":"6","0111":"7",
    "1000":"8","1001":"9","1010":"a","1011":"b",
    "1100":"c","1101":"d","1110":"e","1111":"f",    
}

def bin8toNum (d):
    return bin4toNum[d[0:4]] + bin4toNum[d[4:8]]
def reg(r):
    return "r" + bin3toNum[r]

def getCmd(line):
    line = [m.lower() for m in line]
    line = tobin16(line)
    if line[0:2] == "11":
        rs = line[2:5]
        rd = line[5:8]
        op3 = line[8:12]
        d = line[12:16]
        cmddic = {"0000":"add","0001":"sub","0010":"and","0011":"or","0100":"xor","0101":"cmp","0110":"mov"}
        if op3 in cmddic :
            return cmddic[op3] + " " +reg(rd) + "," + reg(rs)
        cmddic = { "1000":"sll","1001":"slr","1010":"srl","1011":"sra",}
        if op3 in cmddic :
            return cmddic[op3] + " " +reg(rs) + "," + d
        if op3 == "1111": return "hlt"
        if op3 == "1100": return "in " + reg(rd)
        if op3 == "1101": return "out " + reg(rs)
    if line[0] == "0" :
        ra = line[2:5]
        rb = line[5:8]
        d = line[8:16]
        op2 = {"00":"ld","01":"st"}[line[0:2]]
        return op2 + " "+ reg(ra) + "," + bin8toNum(d)  + "(" + reg(rb) +  ")"
    if line[0:2] == "10":
        op2 = line[2:5]
        rb = line[5:8]
        d  = line[8:16]
        cmddic = {"000":"li","001":"addi","010":"subi"}
        if op2 in cmddic:
            return cmddic[op2] + " " + reg(rb) +  "," + bin8toNum(d)
        if op2 == "100":
            return "b " + bin8toNum(d)
        if op2 == "111":
            cmddic = {"000":"be","001":"blt","010":"ble","011":"bne"}
            cond = line[5:8]
            return cmddic[cond] + " " + bin8toNum(d)
 
        
while True:
    line = sys.stdin.readline()
    print(getCmd(line))