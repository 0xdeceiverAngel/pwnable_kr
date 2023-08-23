# passcode
```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)

    passcode: setgid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-, for GNU/Linux 2.6.24, BuildID[sha1]=d2b7bd64f70e46b1b0eb7036b35b24a651c3666b, not stripped
```
```=
#include <stdio.h>
#include <stdlib.h>

void login(){
	int passcode1;
	int passcode2;

	printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);

	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);

	printf("checking...\n");
	if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
		exit(0);
        }
}

void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}

int main(){
	printf("Toddler's Secure Login System 1.0 beta.\n");

	welcome();
	login();

	// something after login...
	printf("Now I can safely trust you that you have credential :)\n");
	return 0;
}

```
原本scanf()裡面 要加＆ 

但是 這題沒有加上

如果可以控制passcode 1就可以直接以 passcode的值 為位址寫入  =>  *(passcode)

因為 passcode and name 空間會重複 

hijack print 0804a000 改成  0x080485e3 讓他直接 print flag



- ebp-0xc passcode2
- ebp-0x10 passcode1 寫上 0x804a000 
- ebp-0x70 name[100]

>0x70-0xc = 100


```c=
08048420 <printf@plt>:
 8048420:       ff 25 00 a0 04 08       jmp    DWORD PTR ds:0x804a000
 8048426:       68 00 00 00 00          push   0x0
 804842b:       e9 e0 ff ff ff          jmp    8048410 <.plt>

08048564 <login>:
 8048564:       55                      push   ebp
 8048565:       89 e5                   mov    ebp,esp
 8048567:       83 ec 28                sub    esp,0x28
 804856a:       b8 70 87 04 08          mov    eax,0x8048770
 804856f:       89 04 24                mov    DWORD PTR [esp],eax
 8048572:       e8 a9 fe ff ff          call   8048420 <printf@plt>
 8048577:       b8 83 87 04 08          mov    eax,0x8048783
 804857c:       8b 55 f0                mov    edx,DWORD PTR [ebp-0x10]
 804857f:       89 54 24 04             mov    DWORD PTR [esp+0x4],edx
 8048583:       89 04 24                mov    DWORD PTR [esp],eax
 8048586:       e8 15 ff ff ff          call   80484a0 <__isoc99_scanf@plt>
 804858b:       a1 2c a0 04 08          mov    eax,ds:0x804a02c
 8048590:       89 04 24                mov    DWORD PTR [esp],eax
 8048593:       e8 98 fe ff ff          call   8048430 <fflush@plt>
 8048598:       b8 86 87 04 08          mov    eax,0x8048786
 804859d:       89 04 24                mov    DWORD PTR [esp],eax
 80485a0:       e8 7b fe ff ff          call   8048420 <printf@plt>
 80485a5:       b8 83 87 04 08          mov    eax,0x8048783
 80485aa:       8b 55 f4                mov    edx,DWORD PTR [ebp-0xc]
 80485ad:       89 54 24 04             mov    DWORD PTR [esp+0x4],edx
 80485b1:       89 04 24                mov    DWORD PTR [esp],eax
 80485b4:       e8 e7 fe ff ff          call   80484a0 <__isoc99_scanf@plt>
 80485b9:       c7 04 24 99 87 04 08    mov    DWORD PTR [esp],0x8048799
 80485c0:       e8 8b fe ff ff          call   8048450 <puts@plt>
 80485c5:       81 7d f0 e6 28 05 00    cmp    DWORD PTR [ebp-0x10],0x528e6
 80485cc:       75 23                   jne    80485f1 <login+0x8d>
 80485ce:       81 7d f4 c9 07 cc 00    cmp    DWORD PTR [ebp-0xc],0xcc07c9
 80485d5:       75 1a                   jne    80485f1 <login+0x8d>
 80485d7:       c7 04 24 a5 87 04 08    mov    DWORD PTR [esp],0x80487a5
 80485de:       e8 6d fe ff ff          call   8048450 <puts@plt>
 80485e3:       c7 04 24 af 87 04 08    mov    DWORD PTR [esp],0x80487af
 80485ea:       e8 71 fe ff ff          call   8048460 <system@plt>

```












