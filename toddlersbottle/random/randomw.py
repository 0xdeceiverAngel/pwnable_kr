from pwn import *
context.log_level = 'DEBUG'
r = process('./random')
# r = remote('pwnable.kr',9000)

# raw_input("#")
# r.recvuntil(":")

r.sendline('3039230856')


r.interactive()
