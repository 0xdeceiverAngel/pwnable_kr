# ascii_easy

**未完成**

這一題有給 libc-2.15.so

```
ascii_easy@pwnable:~$ checksec ascii_easy
[*] '/home/ascii_easy/ascii_easy'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

有 overflow 且用輸入只吃 ascii ，想辦法跳上 libc

system 無法跳
```
pwndbg> print system
$1 = {int (const char *)} 0xf7c48150 <__libc_system>
```

onegadget 也無法
```
0x3ed77 execve("/bin/sh", esp+0x148, environ)
constraints:
  ebx is the GOT address of libc
  [esp+0x148] == NULL

0x6667f execl("/bin/sh", "sh", [esp+0x8])
constraints:
  ebx is the GOT address of libc
  [esp+0x8] == NULL

0x66685 execl("/bin/sh", eax)
constraints:
  ebx is the GOT address of libc
  eax == NULL

0x66689 execl("/bin/sh", [esp+0x4])
constraints:
  ebx is the GOT address of libc
  [esp+0x4] == NULL
```



```
user@vm-ubuntu20:~/pwnablekr/pwnable_kr$ objdump -d -Mintel libc-2.15.so |grep  execve
objdump: Warning: Separate debug info file libc-2.15.so found, but CRC does not match - ignoring
objdump: Warning: Separate debug info file /home/user/pwnablekr/pwnable_kr/libc-2.15.so found, but CRC does not match - ignoring
   3edab:       e8 30 98 07 00          call   b85e0 <execve@@GLIBC_2.0>
000b85e0 <execve@@GLIBC_2.0>:
   b8616:       77 0b                   ja     b8623 <execve@@GLIBC_2.0+0x43>
   b8631:       eb e5                   jmp    b8618 <execve@@GLIBC_2.0+0x38>
000b8640 <fexecve@@GLIBC_2.0>:
   b8684:       0f 84 7e 00 00 00       je     b8708 <fexecve@@GLIBC_2.0+0xc8>
   b8691:       75 75                   jne    b8708 <fexecve@@GLIBC_2.0+0xc8>
   b8695:       74 71                   je     b8708 <fexecve@@GLIBC_2.0+0xc8>
   b86c4:       e8 17 ff ff ff          call   b85e0 <execve@@GLIBC_2.0>
   b86f2:       74 0c                   je     b8700 <fexecve@@GLIBC_2.0+0xc0>
   b8703:       eb 10                   jmp    b8715 <fexecve@@GLIBC_2.0+0xd5>
   b876a:       e8 71 fe ff ff          call   b85e0 <execve@@GLIBC_2.0>
   b8802:       e8 d9 fd ff ff          call   b85e0 <execve@@GLIBC_2.0>
   b88c9:       e8 12 fd ff ff          call   b85e0 <execve@@GLIBC_2.0>
   b8967:       e8 74 fc ff ff          call   b85e0 <execve@@GLIBC_2.0>
   b8a32:       e8 a9 fb ff ff          call   b85e0 <execve@@GLIBC_2.0>
   b8c1b:       e8 c0 f9 ff ff          call   b85e0 <execve@@GLIBC_2.0>
   b8cda:       e8 01 f9 ff ff          call   b85e0 <execve@@GLIBC_2.0>
   b8e01:       e8 da f7 ff ff          call   b85e0 <execve@@GLIBC_2.0>
   b8ea8:       e8 33 f7 ff ff          call   b85e0 <execve@@GLIBC_2.0>
   d8b77:       e8 64 fa fd ff          call   b85e0 <execve@@GLIBC_2.0>
   d8eb5:       e8 26 f7 fd ff          call   b85e0 <execve@@GLIBC_2.0>
   d91ae:       e8 2d f4 fd ff          call   b85e0 <execve@@GLIBC_2.0>
   da486:       e8 55 e1 fd ff          call   b85e0 <execve@@GLIBC_2.0>
```

`0x5561676a` `b876a` 可以跳，剩下就是找參數 


```c=
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>

#define BASE ((void*)0x5555e000)

int is_ascii(int c){
    if(c>=0x20 && c<=0x7f) return 1;
    return 0;
}

void vuln(char* p){
    char buf[20];
    strcpy(buf, p);
}

void main(int argc, char* argv[]){

    if(argc!=2){
        printf("usage: ascii_easy [ascii input]\n");
        return;
    }

    size_t len_file;
    struct stat st;
    int fd = open("/home/ascii_easy/libc-2.15.so", O_RDONLY);
    if( fstat(fd,&st) < 0){
        printf("open error. tell admin!\n");
        return;
    }

    len_file = st.st_size;
    if (mmap(BASE, len_file, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE, fd, 0) != BASE){
        printf("mmap error!. tell admin\n");
        return;
    }

    int i;
    for(i=0; i<strlen(argv[1]); i++){
        if( !is_ascii(argv[1][i]) ){
            printf("you have non-ascii byte!\n");
            return;
        }
    }

    printf("triggering bug...\n");
    vuln(argv[1]);

}

```


