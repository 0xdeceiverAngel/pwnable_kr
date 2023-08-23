# flag
```=
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
    Packer:   Packed with UPX

```
有 UPX壓縮
```=
upx -d flag  
```
解開 看adm
```=
;-- main:
/ (fcn) sym.main 61
|   sym.main (int argc, char **argv, char **envp);
|           ; var int local_8h @ rbp-0x8
|           ; DATA XREF from entry0 (0x401075)
|           0x00401164      55             push rbp
|           0x00401165      4889e5         mov rbp, rsp
|           0x00401168      4883ec10       sub rsp, 0x10
|           0x0040116c      bf58664900     mov edi, str.I_will_malloc___and_strcpy_the_flag_there._take_it. ; 0x496658 ; "I will malloc() and strcpy the flag there. take it."
|           0x00401171      e80a0f0000     call sym.puts               ; int puts(const char *s)
|           0x00401176      bf64000000     mov edi, 0x64               ; 'd' ; 100
|           0x0040117b      e850880000     call sym.malloc             ; sym.malloc_set_state+0x560
|           0x00401180      488945f8       mov qword [local_8h], rax
|           0x00401184      488b15e50e2c.  mov rdx, qword obj.flag     ; [0x6c2070:8]=0x496628 str.UPX...__sounds_like_a_delivery_service_: ; "(fI"
|           0x0040118b      488b45f8       mov rax, qword [local_8h]
|           0x0040118f      4889d6         mov rsi, rdx
|           0x00401192      4889c7         mov rdi, rax
|           0x00401195      e886f1ffff     call fcn.00400320
|           0x0040119a      b800000000     mov eax, 0
|           0x0040119f      c9             leave
\           0x004011a0      c3             ret

```

用 gdb 看

```=
RAX: 0x6c96b0 --> 0x0
RBX: 0x401ae0 (<__libc_csu_fini>:	push   rbx)
RCX: 0x8
RDX: 0x496628 ("UPX...? sounds like a delivery service :)")  //here
RSI: 0x0
RDI: 0x4
RBP: 0x7fffffffdec0 --> 0x0
RSP: 0x7fffffffdeb0 --> 0x401a50 (<__libc_csu_init>:	push   r14)
RIP: 0x40118f (<main+43>:	mov    rsi,rdx)
R8 : 0x1
R9 : 0x3
R10: 0x22 ('"')
R11: 0x0
R12: 0x401a50 (<__libc_csu_init>:	push   r14)
R13: 0x0
R14: 0x0
R15: 0x0
EFLAGS: 0x202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x401180 <main+28>:	mov    QWORD PTR [rbp-0x8],rax
   0x401184 <main+32>:	mov    rdx,QWORD PTR [rip+0x2c0ee5]        # 0x6c2070 <flag>
   0x40118b <main+39>:	mov    rax,QWORD PTR [rbp-0x8]
=> 0x40118f <main+43>:	mov    rsi,rdx
   0x401192 <main+46>:	mov    rdi,rax
   0x401195 <main+49>:	call   0x400320
   0x40119a <main+54>:	mov    eax,0x0
   0x40119f <main+59>:	leave
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdeb0 --> 0x401a50 (<__libc_csu_init>:	push   r14)
0008| 0x7fffffffdeb8 --> 0x6c96b0 --> 0x0
0016| 0x7fffffffdec0 --> 0x0
0024| 0x7fffffffdec8 --> 0x401344 (<__libc_start_main+404>:	mov    edi,eax)
0032| 0x7fffffffded0 --> 0x0
0040| 0x7fffffffded8 --> 0x100000000
0048| 0x7fffffffdee0 --> 0x7fffffffdfb8 --> 0x7fffffffe31e ("/home/user/下載/pwnablekr/flag/flag")
0056| 0x7fffffffdee8 --> 0x401164 (<main>:	push   rbp)
[------------------------------------------------------------------------------]
```
看 rdx 
