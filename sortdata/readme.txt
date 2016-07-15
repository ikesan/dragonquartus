# コードの変換を確認する
#   $cat <コードを書いたテキスト> | python3 replace.py 
# 以下,readme.txt を <コードを書いたテキスト> とした例を示す
# - コードの確認 
#   $cat readme.txt | python3 replace.py 
# - 16進数4桁のアセンブリに変換
#   $cat readme.txt | python3 replace.py -n -c
# - mif形式に変換
#   $cat readme.txt | python3 replace.py -n -c | python3 code2mif.py
# - a.mifに変換して書き出す
#   $cat readme.txt | python3 replace.py -n -c | python3 code2mif.py > a.mif

# 普通にアセンブリを描くことができる
b 0x02
add r0,r1
addi r0,03
st r4,00(r0)
ld r4,00(r0)
# 普通のコードみたいに描くこともできる
r0 -= 2
r0 += r1
r4 += 2
r7 = r4
r6 - r4
r5 - 3
r2 <<= 2
mem[r0+2] = r4
r4 = mem[r0+2] 
hlt

# - ソートコード生成
#   $cat random.mif | python3 mergesort.py -n | python3 replace.py -n -c | python3 code2mif.py
# - ソートデータをシフトする
#   $cat r_sorted.mif | python3 shiftmif.py > r_sorted2.mif