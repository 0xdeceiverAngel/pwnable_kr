# fd

ssh 連上

```=
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
	if(argc<2){
		printf("pass argv[1] a number\n");
		return 0;
	}
	int fd = atoi( argv[1] ) - 0x1234;
	int len = 0;
	len = read(fd, buf, 32);
	if(!strcmp("LETMEWIN\n", buf)){
		printf("good job :)\n");
		system("/bin/cat flag");
		exit(0);
	}
	printf("learn about Linux file IO\n");
	return 0;

}

```
Let fd be 0 ,read from stdin

0x1234 = 4660
```=
fd@pwnable:~$ ./fd  4660
LETMEWIN
good job :)
mommy! I think I know what a file descriptor is!!


fd@pwnable:~$ ./fd  4661
LETMEWIN
good job :)
mommy! I think I know what a file descriptor is!!

```
