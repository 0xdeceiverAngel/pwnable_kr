# leg

這邊可以直接看leg.asm 比較清楚

## 網路上解法 眾說紛紜 
這題搞好久 查了write up 才知道是它的組語是 arm 架構

難怪一直解不出來

暫存器 pc 會儲存 ~~當前的addr+8~~ 或 pc為進接的第二條指令的地址

後來發現 不一定 要以`pc為進接的第二條指令的地址`才準確

bx 作為切換

`key2+16处bx跳转到key+20（指令地址会先和0xFFFFFFFE进行按位与，因为最后一位肯定是0，因此最后一位用于做标志位，bx执行时如果地址最后一位是0，表示跳到arm状态，1则跳到thumb态），因为地址最低位是1，所以切换为thumb状态。`

因為有可能`從原本arm mode切換至thumb mode` 也可以從
```
instruction<+12>
instruction<+16>
```
看出offset是4  變成pc+4

`至於為啥它要怎切換 我還沒研究`

以前在課本上學到的是 pc 會存下一個 instruction 為啥跟學到的不一樣？

why? https://www.cnblogs.com/douzi2/p/4934202.html  這裡有解釋 就是 因為 pipline技術

暫存器 lr 會儲存 當前的ret addr `lr in ARM is Link Register`

r0 作為返回值

所以 key1+2+3=`0x00008cdc+0x8`+`0x00008d04+0x4+0x4`+`0x00008d80`=108400