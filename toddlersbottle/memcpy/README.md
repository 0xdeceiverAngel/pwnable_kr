# memcpy


輸入10個數字，分別位於2的各次冪之間

movdqa movntps 對記憶體操作要對齊 16 bytes

malloc 32 bit 對齊 8 bytes

malloc 64 bit 對齊 16 bytes

malloc 實際上會多分配 4 bytes


```python
# both work
n=3
for a in range(0,6000):
    
    if (a + 4) % 16 > 9  :

        if a>2**n and a<2**(n+1):
            print(a , end= ' ' )
            n=n+1
            
            
            
# 9 22 38 70 134 262 518 1030 2054 4102 

n=3
for a in range(0,6000):
    
    if (a + 4) % 16 ==0 :
        if a>2**n and a<2**(n+1):
            print(a , end= ' ' )
            n=n+1
            
            
# 12 28 44 76 140 268 524 1036 2060 4108 
```

```
echo "12 28 44 76 140 268 524 1036 2060 4108 " | nc 0 9022
```