from pwn import *
import time
context.log_level = 'DEBUG'
def chk(s,n,c):
    left=s
    right=n

    for i in range(c):
        mid=(left+right)/2
        result=auto(left,mid)
        if(result==0):

            left=mid+1

        if(result==1):

            right=mid

    # r.interactive()
    r.sendline(str(left))
    r.recv()
def auto(s,n):
    send=" "
    for i in range(s,n+1):
        send+=str(i)
        send+=' '
    r.sendline(send)
    re=r.recv()
    # if(re=='format error\n'):
        # r.interactive()
    # if(c==0):
        # r.sendline(int(n))
    if((int(re))%10==0):
        # print '1'
        # log.info('1')
        # auto(n/2,n,c-1)
        return 0
    else:
        # auto(0,n/2,c-1)
        return 1
    # log.info(re)
r=remote('pwnable.kr',9007)
r.read()
time.sleep(4)
for i in range(100):
    str0=r.recv()
    # log.info(str)
    str0=str0.strip()
    log.info(str0)
    str1=str0.split(' ')[0]
    # log.info(str1)
    str2=str0.split(' ')[1]
    # log.info(str2)
    n=str1.split('=')[1]
    c=str2.split('=')[1]
    # log.info(n)
    # log.info(c)
    chk(0,int(n),int(c))
