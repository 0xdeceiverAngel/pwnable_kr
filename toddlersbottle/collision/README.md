# col
```=
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}

```

`*p` 是 char 指標

`(int *)p` 強制把 `char 指標` 轉成 `int 指標`


int 4byte

所以它會一次讀4byte

0x21DD09EC / 5 = 0x6C5CEC8*4 +0x4

剛好湊到長度20

```=
./col `python -c 'print "\xc8\xce\xc5\x06"*4 +"\xcc\xce\xc5\x06"'`
```
