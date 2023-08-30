# otp

file name 是 opt 的前 4 bytes ，內容是後 4 bytes

ulimit -f 0 

去限制寫入的大小為0

但是設定完之後跑會

```
ulimit -f 0 
otp@pwnable:~$ ./otp 00
File size limit exceeded (core dumped)
```

如果將文件大小限制設置為 0，則可以自由讀取文件，但寫入文件時會發出信號，所以阻止訊號

>ulimit -f 0 && python -c "import os, signal; signal.signal(signal.SIGXFSZ, signal.SIG_IGN); os.system('./otp 0')"

>ulimit -f
>trap '' SIGXFSZ
>./otp 0

```
otp@pwnable:~$ ulimit -f 0
otp@pwnable:~$ python
Python 2.7.12 (default, Mar  1 2021, 11:38:31) 
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> os.system("./otp 1")
OTP generated.
OTP mismatch
0
>>> os.system("./otp 0")
OTP generated.
Congratz!
Darn... I always forget to check the return value of fclose() :(
0
```

```c=
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>

int main(int argc, char* argv[]){
    char fname[128];
    unsigned long long otp[2]; // 8 bytes

    if(argc!=2){
        printf("usage : ./otp [passcode]\n");
        return 0;
    }

    int fd = open("/dev/urandom", O_RDONLY);
    if(fd==-1) exit(-1);

    if(read(fd, otp, 16)!=16) exit(-1);
    close(fd);

    sprintf(fname, "/tmp/%llu", otp[0]);
    FILE* fp = fopen(fname, "w");
    if(fp==NULL){ exit(-1); }
    fwrite(&otp[1], 8, 1, fp);
    fclose(fp);

    printf("OTP generated.\n");

    unsigned long long passcode=0;
    FILE* fp2 = fopen(fname, "r");
    if(fp2==NULL){ exit(-1); }
    fread(&passcode, 8, 1, fp2);
    fclose(fp2);
    
    if(strtoul(argv[1], 0, 16) == passcode){
        printf("Congratz!\n");
        system("/bin/cat flag");
    }
    else{
        printf("OTP mismatch\n");
    }

    unlink(fname);
    return 0;
}
```

