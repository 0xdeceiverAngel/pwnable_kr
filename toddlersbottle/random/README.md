# random
原本想要 buf 讓 rand 值和 input 可控 結果不行

~~可能因為  input 往下overflow~~

~~只會壓到 rbp 等 壓不到 random~~

~~或是~~

因為它只吃int 大小的4byte 所以 所以不會overflow

解法：

seed 是固定的 

rand 值是固定的 

6b8b4567 xor deadbeef = B526FB88 = 3039230856(dec)

輸入 3039230856 

```=
;           ; var int local_8h @ rbp-0x8  input
|           ; var int local_4h @ rbp-0x4  random 值
|           ; DATA XREF from entry0 (0x40052d)
|           0x004005f4      55             push rbp
|           0x004005f5      4889e5         mov rbp, rsp
|           0x004005f8      4883ec10       sub rsp, 0x10
|           0x004005fc      b800000000     mov eax, 0
|           0x00400601      e8fafeffff     call sym.imp.rand           ; int rand(void)
|           0x00400606      8945fc         mov dword [local_4h], eax
|           0x00400609      c745f8000000.  mov dword [local_8h], 0
|           0x00400610      b860074000     mov eax, 0x400760
|           0x00400615      488d55f8       lea rdx, qword [local_8h]
|           0x00400619      4889d6         mov rsi, rdx
|           0x0040061c      4889c7         mov rdi, rax
|           0x0040061f      b800000000     mov eax, 0
|           0x00400624      e8c7feffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
|           0x00400629      8b45f8         mov eax, dword [local_8h]
|           0x0040062c      3345fc         xor eax, dword [local_4h]
|           0x0040062f      3defbeadde     cmp eax, 0xdeadbeef
|       ,=< 0x00400634      7520           jne 0x400656
|       |   0x00400636      bf63074000     mov edi, str.Good           ; 0x400763 ; "Good!"
|       |   0x0040063b      e880feffff     call sym.imp.puts           ; int puts(const char *s)
|       |   0x00400640      bf69074000     mov edi, str.bin_cat_flag   ; 0x400769 ; "/bin/cat flag"
|       |   0x00400645      b800000000     mov eax, 0
|       |   0x0040064a      e881feffff     call sym.imp.system         ; int system(const char *string)
|       |   0x0040064f      b800000000     mov eax, 0
|      ,==< 0x00400654      eb0f           jmp 0x400665
|      |`-> 0x00400656      bf78074000     mov edi, str.Wrong__maybe_you_should_try_2_32_cases. ; 0x400778 ; "Wrong, maybe you should try 2^32 cases."
|      |    0x0040065b      e860feffff     call sym.imp.puts           ; int puts(const char *s)
|      |    0x00400660      b800000000     mov eax, 0
|      |    ; CODE XREF from main (0x400654)
|      `--> 0x00400665      c9             leave
\           0x00400666      c3             ret
```
