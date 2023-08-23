n=3
for a in range(0,6000):
    
    if (a + 4) % 16 > 9 or (a + 4) % 16 ==0 :
        if a>2**n and a<2**(n+1):
            print(a , end= ' ' )
            n=n+1