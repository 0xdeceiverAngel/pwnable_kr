```
horcruxes@pwnable:~$ checksec horcruxes 
[*] '/home/horcruxes/horcruxes'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x809f000)
```

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // ST1C_4

  setvbuf(stdout, 0, 2, 0);
  setvbuf(stdin, 0, 2, 0);
  alarm(0x3Cu);
  hint();
  init_ABCDEFG();
  v3 = seccomp_init(0);
  seccomp_rule_add(v3, 2147418112, 173, 0);
  seccomp_rule_add(v3, 2147418112, 5, 0);
  seccomp_rule_add(v3, 2147418112, 3, 0);
  seccomp_rule_add(v3, 2147418112, 4, 0);
  seccomp_rule_add(v3, 2147418112, 252, 0);
  seccomp_load(v3);
  return ropme();
}
```

第一個想法是hook urandom 

```c=
unsigned int init_ABCDEFG()
{
  int v0; // eax
  unsigned int result; // eax
  unsigned int buf; // [esp+8h] [ebp-10h]
  int fd; // [esp+Ch] [ebp-Ch]

  fd = open("/dev/urandom", 0);
  if ( read(fd, &buf, 4u) != 4 )
  {
    puts("/dev/urandom error");
    exit(0);
  }
  close(fd);
  srand(buf);
  a = -559038737 * rand() % 0xCAFEBABE;
  b = -559038737 * rand() % 0xCAFEBABE;
  c = -559038737 * rand() % 0xCAFEBABE;
  d = -559038737 * rand() % 0xCAFEBABE;
  e = -559038737 * rand() % 0xCAFEBABE;
  f = -559038737 * rand() % 0xCAFEBABE;
  v0 = rand();
  g = -559038737 * v0 % 0xCAFEBABE;
  result = f + e + d + c + b + a + -559038737 * v0 % 0xCAFEBABE;
  sum = result;
  return result;
}
```

gets 這邊有 overflow

但是沒辦法直接跳上 open file ，因為read 遇到 0xA 就會截斷

發現走正常流程會需要 a~g 和的值

所以構造 rop 跳上 a~g 取得所有的值 再跳回 ropme 輸入sum



```
 80a010b:       83 ec 08                sub    esp,0x8
 80a010e:       6a 00                   push   0x0
 80a0110:       68 3c 05 0a 08          push   0x80a053c
 80a0115:       e8 a6 fb ff ff          call   809fcc0 <open@plt>
 80a011a:       83 c4 10                add    esp,0x10
 80a011d:       89 45 f4                mov    DWORD PTR [ebp-0xc],eax
 80a0120:       83 ec 04                sub    esp,0x4
 80a0123:       6a 64                   push   0x64
 80a0125:       8d 45 8c                lea    eax,[ebp-0x74]
 80a0128:       50                      push   eax
 80a0129:       ff 75 f4                push   DWORD PTR [ebp-0xc]
 80a012c:       e8 ff fa ff ff          call   809fc30 <read@plt>
```

```c=

int ropme()
{
  char s[100]; // [esp+4h] [ebp-74h]
  int input; // [esp+68h] [ebp-10h]
  int fd; // [esp+6Ch] [ebp-Ch]

  printf("Select Menu:");
  __isoc99_scanf("%d", &input);
  getchar();
  if ( input == a )
  {
    A();
  }
  else if ( input == b )
  {
    B();
  }
  else if ( input == c )
  {
    C();
  }
  else if ( input == d )
  {
    D();
  }
  else if ( input == e )
  {
    E();
  }
  else if ( input == f )
  {
    F();
  }
  else if ( input == g )
  {
    G();
  }
  else
  {
    printf("How many EXP did you earned? : ");
    gets(s);
    if ( atoi(s) == sum )
    {
      fd = open("flag", 0);
      s[read(fd, s, 0x64u)] = 0;
      puts(s);
      close(fd);
      exit(0);
    }
    puts("You'd better get more experience to kill Voldemort");
  }
  return 0;
}
```
payload 如果計算 sum 就送會很不穩定

init_abcdefg 再算sum的時候用 unsigned int ，所以收到並加總後要取 unsign_int_max 餘數，確保在 unsign_int_max 內

gets 後

atoi 回傳是 int ，所以如果取完餘數後>int_max 會導致 overflow 到 signed bit ，所以要再減掉 unsign_int_max