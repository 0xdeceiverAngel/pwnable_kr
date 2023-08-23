# input
這題當初看了也是一頭霧水 黑人問號

但是這題也學到很多東西

首先
```=
SYNOPSIS
       #include <unistd.h>

       int execve(const char *filename, char *const argv[],char *const envp[]);

```

第一階

它要 100個引數 所以就用 `execve` 去給它引數


第二階

會吃4byte 2次 分別fd是0 2

要用pipe解

而 pipe 看了超久

裡面有個pipe.c 練習的

反正就是
```
要先宣告 fd
建立pipe
fork 多工
關閉pipe
dup2重新導向
```
J個 寫的很好 ![pipe](https://hengxiuxu.blogspot.com/2015/10/linux-fork-pipe.html)

第三階

比較環境變數

用execve傳入環境變數

這裡結尾跟參數一樣 都是 NULL

第四階

比較檔案內的資料

用fopen就可以建立檔案 再 寫入資料

第五階

input自己建立server 等封包

![](http://i.imgur.com/cqr4O2P.png)
```=
int sd, cd;
struct sockaddr_in saddr, caddr; //store server side ip and port
sd = socket(AF_INET, SOCK_STREAM, 0); //ipv4 tcp protocol default
if(sd == -1){
  printf("socket error, tell admin\n");
  return 0;
}
saddr.sin_family = AF_INET;//ipv4
saddr.sin_addr.s_addr = INADDR_ANY;
saddr.sin_port = htons( atoi(argv['C']) );
if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
  printf("bind error, use another port\n");
      return 1;
}
listen(sd, 1);
int c = sizeof(struct sockaddr_in);
cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
if(cd < 0){
  printf("accept error, tell admin\n");
  return 0;
}
if( recv(cd, buf, 4, 0) != 4 ) return 0;
if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
```
所以就再fork

小孩子執行input 爸爸執行socket client

然後input server 開的 port 我們argv['C']的參數

最後就是在ssh上 /tmp 裡建立資料夾 編譯我們的 payload.c

連結 flag and input

執行payload
