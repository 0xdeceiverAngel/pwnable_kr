# mistake

沒有bof

題目有提示 ：operator priority

而且執行起來會卡住 然後等輸入 之後才會進 等input passwor輸入

`<`的優先權比`=`高

```=
if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0)
變成 先做
open("/home/mistake/password",O_RDONLY,0400) < 0
比較後是0
之後指定 fd=0
```
然後就會下面這行就會變成等輸入 所以才會開頭提到等輸入
```=
if(!(len=read(fd,pw_buf,PW_LEN) > 0))
```
之後就好辦了 知道 `可控`xor`1`=`可控`
```=
mistake@prowl:~$ ./mistake
do not bruteforce...
0000000000  
input password : 1111111111
Password OK
Mommy, the operator priority always confuses me :(
```
