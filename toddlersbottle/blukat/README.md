# blukat

password 可以被 blukat_pwn 組員讀，剛好我們也在組內，直接讀

發現 password 混肴視聽 假裝沒權限 

所以直接cat pipe 到執行檔就可以了


```bash=
blukat@pwnable:~$ whoami
blukat
blukat@pwnable:~$ id
uid=1104(blukat) gid=1104(blukat) groups=1104(blukat),1105(blukat_pwn)

blukat@pwnable:~$ ls -l
total 20
-r-xr-sr-x 1 root blukat_pwn 9144 Aug  8  2018 blukat
-rw-r--r-- 1 root root        645 Aug  8  2018 blukat.c
-rw-r----- 1 root blukat_pwn   33 Jan  6  2017 password

blukat@pwnable:~$ cat password | ./blukat
guess the password!
congrats! here is your flag: Pl3as_DonT_Miss_youR_GrouP_Perm!!


blukat@pwnable:~$ cat password 
cat: password: Permission denied
blukat@pwnable:~$ xxd password
00000000: 6361 743a 2070 6173 7377 6f72 643a 2050  cat: password: P
00000010: 6572 6d69 7373 696f 6e20 6465 6e69 6564  ermission denied
```

```c=
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
char flag[100];
char password[100];
char* key = "3\rG[S/%\x1c\x1d#0?\rIS\x0f\x1c\x1d\x18;,4\x1b\x00\x1bp;5\x0b\x1b\x08\x45+";
void calc_flag(char* s){
        int i;
        for(i=0; i<strlen(s); i++){
                flag[i] = s[i] ^ key[i];
        }
        printf("%s\n", flag);
}
int main(){
        FILE* fp = fopen("/home/blukat/password", "r");
        fgets(password, 100, fp);
        char buf[100];
        printf("guess the password!\n");
        fgets(buf, 128, stdin);
        if(!strcmp(password, buf)){
                printf("congrats! here is your flag: ");
                calc_flag(password);
        }
        else{
                printf("wrong guess!\n");
                exit(0);
        }
        return 0;
}

```