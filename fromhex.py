import sys,re
from tohex import * 

def tobin16(line): return "".join([num_bin4[line[i]] for i in range(4)])
def bin8_num2(d): return bin4_num[d[0:4]] + bin4_num[d[4:8]]
def reg(r): return "r" + bin3_num[r]

def getCmd(line):
    line = [m.lower() for m in line]
    line = tobin16(line)
    if line[0:2] == "11":
        rs,rd,op3,d = line[2:5],line[5:8],line[8:12],line[12:16]
        if op3 in bin_cmd["alu"] :
            return bin_cmd["alu"][op3] + " " +reg(rd) + "," + reg(rs)
        if op3 in bin_cmd["shift"] :
            return bin_cmd["shift"][op3] + " " +reg(rs) + "," + bin4_num[d]
        if op3 == "1111": return "hlt"
        if op3 == "1100": return "in " + reg(rd)
        if op3 == "1101": return "out " + reg(rs)
    if line[0] == "0" :
        op2,ra,rb,d = line[0:2],line[2:5],line[5:8],line[8:16]
        return bin_cmd["addr"][op2]+" "+reg(ra)+","+bin8_num2(d)+"("+reg(rb)+")"
    if line[0:2] == "10":
        op2,rb,d = line[2:5],line[5:8],line[8:16]
        if op2 in bin_cmd["imm"]:
            return bin_cmd["imm"][op2] + " " + reg(rb) +  "," + bin8_num2(d)
        if op2 == "100": 
            return "b " + bin8_num2(d)
        if op2 == "111":
            cond = line[5:8]
            return bin_cmd["b"][cond] + " " + bin8_num2(d)
 
if __name__ == "__main__" :         
    while True:
        line = sys.stdin.readline()
        print(getCmd(line))