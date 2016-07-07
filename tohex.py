#grammer
#reg := r0 .. r7
#[add/sub/and/or/xor/cmp/mov] reg,reg
#[sll/slr/srl/sra] reg, A (16進数1桁)
#[li/addi/subi] reg,AA (16進数2桁)
#[b/be/blt/ble/bne] AA (16進数2桁)
#[in/out] reg
#hlt
#[ld/st] reg,AA(reg) (16進数2桁)


import sys,re
if __name__ != "__main__" : exit(0)
    

def bin2hex(bin16):
    bindic = {
        "0000": "0","0001": "1","0010": "2","0011": "3",
        "0100": "4","0101": "5","0110": "6","0111": "7",
        "1000": "8","1001": "9","1010": "a","1011": "b",
        "1100": "c","1101": "d","1110": "e","1111": "f",
    }
    #0000111100001111 -> 0f0f
    res  = bindic[bin16[0:4]]
    res += bindic[bin16[4:8]]
    res += bindic[bin16[8:12]]
    res += bindic[bin16[12:16]]
    return res

num2bin3 = {
    "0":"000","1":"001","2":"010","3":"011",
    "4":"100","5":"101","6":"110","7":"111"
}
num2bin4 = {
    "0":"0000","1":"0001","2":"0010","3":"0011",
    "4":"0100","5":"0101","6":"0110","7":"0111",
    "8":"1000","9":"1001","a":"1010","b":"1011",
    "c":"1100","d":"1101","e":"1110","f":"1111",    
}
def num2bin8(d):
    if len(d) == 1:
        return "0000" + num2bin4[d]
    return num2bin4[d[0]] + num2bin4[d[1]]

def getBin(line):
    match = re.findall(r'(add|sub|and|or|xor|cmp|mov)[ ,]r?([0-7])[ ,]r?([0-7])',line,re.I )     
    if match :        
        match = [m.lower() for m in match[0]]
        cmddic = {"add":"0000","sub":"0001","and":"0010","or":"0011","xor":"0100","cmp":"0101","mov":"0110"}
        return bin2hex("11" + num2bin3[match[2]] + num2bin3[match[1]]+cmddic[match[0]] + "0000")

    match = re.findall(r'(sll|slr|srl|sra)[ ,]r?([0-7])[ ,]([0-9a-f])',line,re.I)
    if match :        
        match = [m.lower() for m in match[0]]
        cmddic = { "sll":"1000","slr":"1001","srl":"1010","sra":"1011",}
        return bin2hex("11" + "000" + num2bin3[match[1]]+cmddic[match[0]] + num2bin4[match[2]])

    match = re.findall(r'(li|addi|subi)[ ,]r?([0-7])[ ,]([0-9a-f]{1,2})',line,re.I)
    if match :        
        match = [m.lower() for m in match[0]]
        cmddic = { "li":"000","addi":"001","subi":"010"}
        return bin2hex("10" + cmddic[match[0]] + num2bin3[match[1]] + num2bin8(match[2]))

    match = re.findall(r'(b|be|blt|ble|bne)[ ,]([0-9a-f]{1,2})',line,re.I)
    if match :        
        match = [m.lower() for m in match[0]]
        if match[0] == "b":
            return bin2hex("10100000" + num2bin8(match[1]))
        cmddic = {"be":"000","blt":"001","ble":"010","bne":"011"}
        return bin2hex("10111"+cmddic[match[0]] + num2bin8(match[1]))

    match = re.findall(r'(in|out)[ ,]r?([0-7])',line,re.I)
    if match :        
        match = [m.lower() for m in match[0]]
        if match[0] == "in":
            return bin2hex("11"+"000"+num2bin3[match[1]] + "1100"+"0000")
        if match[0] == "out":
            return bin2hex("11"+num2bin3[match[1]]+"000" + "1101"+"0000")
        assert(0)

    match = re.findall(r'(hlt)',line,re.I)
    if match : return bin2hex("1111""1111""1111""1111")

    match = re.findall(r'(ld|st)[ ,]r?([0-7])[ ,]([0-9a-f]{2})\(r?([0-7])\)',line,re.I)
    if match :        
        match = [m.lower() for m in match[0]]
        cmddic = { "ld":"00","st":"01"}
        return bin2hex(cmddic[match[0]] + num2bin3[match[1]] + num2bin3[match[3]] + num2bin8(match[2]))
    assert(False)
while True:
    line = sys.stdin.readline()
    print(getBin(line))