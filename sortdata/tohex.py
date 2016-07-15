# 使用例
#add r0,r1 # c800
#sub r0 r1 # c810 (句読点は空白でも可)
#add 0 1   # c800 (レジスタを示す r は省略可能)
#sll r7 f  # c08f (レジスタはr0..r7まで)
#li r0 fe  # 80fe
#b ff      # a0ff
#in r3     # c3c0
#ld r2 AA(r1) # 11aa

import sys,re

def reverseDic(dic) : 
    return { v:k for k,v in dic.items() }

num_bin3 = {
    "0":"000","1":"001","2":"010","3":"011",
    "4":"100","5":"101","6":"110","7":"111",
}
bin3_num = reverseDic(num_bin3)
num_bin4 = {
    "0":"0000","1":"0001","2":"0010","3":"0011",
    "4":"0100","5":"0101","6":"0110","7":"0111",
    "8":"1000","9":"1001","a":"1010","b":"1011",
    "c":"1100","d":"1101","e":"1110","f":"1111",    
}
bin4_num = reverseDic(num_bin4)
cmd_bin = {
    "alu" : { "add":"0000","sub":"0001","and":"0010","or":"0011","xor":"0100","cmp":"0101","mov":"0110" },
    "shift" : { "sll":"1000","slr":"1001","srl":"1010","sra":"1011" },
    "imm" : { "li":"000","addi":"001","subi":"010","cmpi":"011" },
    "addr" : { "ld":"00","st":"01" },
    "b": { "be":"000","blt":"001","ble":"010","bne":"011" }
}
bin_cmd = { k:reverseDic(v) for k,v in cmd_bin.items()}

#0000111100001111 => 0f0f
def bin2hex(bin16):
    return "".join([ bin4_num[bin16[4 * i:4 * i + 4]] for i in range(4)])

#ff => 11111111,f => 00001111
def num2_bin8(d):
    if len(d) == 1 : return "0000" + num_bin4[d]
    else : return num_bin4[d[0]] + num_bin4[d[1]]

def getBin(line):
    def getMatched(regex):
        match = re.findall(regex,line,re.I )     
        if match : return [m.lower() for m in match[0]]
        else : return []  
    reg = num_bin3
    d1  = num_bin4  
    d2  = num2_bin8    
    rxreg = r'r?([0-7])'
    sp    = r'[ ,]'
    bit8  = r'(?:0x)?([0-9a-f]{1,2})'
    bit4  = r'([0-9a-f])'
    m = getMatched(r'(add|sub|and|or|xor|cmp|mov)'+sp+rxreg+sp+rxreg)
    if m : return bin2hex("11" + reg[m[2]] + reg[m[1]]+ cmd_bin["alu"][m[0]] + "0000")
    m = getMatched(r'(sll|slr|srl|sra)'+sp+rxreg+sp+bit4)
    if m : return bin2hex("11" + "000" + reg[m[1]]+cmd_bin["shift"][m[0]] + d1[m[2]])
    m = getMatched(r'(li|addi|subi|cmpi)'+sp+rxreg+sp+bit8)
    if m : return bin2hex("10" + cmd_bin["imm"][m[0]] + reg[m[1]] + d2(m[2]))
    m = getMatched(r'(ld|st)'+sp+rxreg+sp+bit8+r'\('+rxreg+r'\)')
    if m : return bin2hex(cmd_bin["addr"][m[0]] + reg[m[1]] + reg[m[3]] + d2(m[2]))
    m = getMatched(r'(b|be|blt|ble|bne)'+sp+bit8)
    if m : 
        if m[0] == "b": return bin2hex("10100000" + d2(m[1]))
        return bin2hex("10111"+cmd_bin["b"][m[0]] + d2(m[1]))
    m = getMatched(r'(in|out)'+sp+rxreg)
    if m :        
        if m[0] == "in": return bin2hex("11"+"000"+reg[m[1]] + "1100"+"0000")
        if m[0] =="out": return bin2hex("11"+reg[m[1]]+"000" + "1101"+"0000")
    if re.findall(r'(hlt)',line,re.I) : return bin2hex("1111""1111""1111""1111")
    ## 以下 簡略表記
    m = getMatched(rxreg+r'\s*=\s*'+bit8)
    if m : return getBin("li r" + m[0] + " " + m[1])
    m = getMatched(rxreg+r'\s*<<=\s*'+bit8)
    if m : return getBin("sll r" + m[0] + " " + m[1])
    m = getMatched(rxreg+r'\s*\+=\s*'+bit8)
    if m : return getBin("addi r" + m[0] + " " + m[1])
    m = getMatched(rxreg+r'\s*-=\s*'+bit8)
    if m : return getBin("subi r" + m[0] + " " + m[1])
    m = re.findall(r'b\s+'+bit8+r'\s*\?.+?(==|!=|<|<=)\s+?0',line )
    if m : 
        bcmd = {"==":"be", "<":"blt", "<=":"ble","!=": "bne"}
        return getBin(bcmd[m[1]] + " " + m[0])
    m = getMatched(rxreg+r'\s*=\s*'+rxreg)
    if m : return getBin("mov r" + m[0] + " r" + m[1])
    m = getMatched(rxreg+r'\s*\+=\s*'+rxreg)
    if m : return getBin("add r" + m[0] + " r" + m[1])
    m = getMatched(rxreg+r'\s*-=\s*'+rxreg)
    if m : return getBin("sub r" + m[0] + " r" + m[1])
    m = getMatched(rxreg+r'\s*=\s*mem\['+rxreg+r'\s*\+\s*'+bit8+r'\]')

    if m : return getBin("ld r" + m[0] + " "+ m[2]+"(r" +m[1]+")")
    m = getMatched(r'mem\['+rxreg+r'\s*\+\s*'+bit8+r'\]\s*=\s*'+rxreg)
    if m : return getBin("st r" + m[2] + " "+ m[1]+"(r" +m[0]+")")

    m = getMatched(rxreg+r'\s*-\s*'+bit8)
    if m : return getBin("cmpi r" + m[0] + " " + m[1])
    m = getMatched(r'r([0-7])\s*-\s*r([0-7])')
    if m : return getBin("cmp r" + m[0] + " r" + m[1])
    return "### ERROR ###"

if __name__ == "__main__" :
    while True:
        line = sys.stdin.readline()
        if not line : exit(0)
        print(getBin(line))