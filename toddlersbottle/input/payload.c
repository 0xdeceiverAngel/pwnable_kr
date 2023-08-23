#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main()
{

  char *argv[101]={"/home/user/Downloads/pwnablekr/input/input",[1 ... 99]="A",NULL};
  argv['A']="\x00";
  argv['B']="\x20\x0a\x0d";
  argv['C']="1234";
  //====================================
  int stdin[2];
  int stderr[2];
  pipe(stdin);
  pipe(stderr);
  pid_t child;
  if((child=fork())==0)
    {

      write(stdin[1],"\x00\x0a\x00\xff",4);
      close(stdin[0]);//close read
      close(stdin[1]);
      write(stderr[1],"\x00\x0a\x02\xff",4);
      close(stderr[0]);//close read
      close(stderr[1]);
      exit(0);
    }
  else
    {

      dup2(stdin[0],0);
      close(stdin[0]);
      close(stdin[1]);
      dup2(stderr[0],2);
      close(stderr[0]);
      close(stderr[1]);

    }


    FILE* fp = fopen("\x0a","w");
    fwrite("\x00\x00\x00\x00",4,1,fp);
    fclose(fp);





    char *env[2] = {"\xde\xad\xbe\xef=\xca\xfe\xba\xbe", NULL};


    if((child=fork())==0)
      {

          execve("input",argv,env);
      }
    else
      {
        sleep(1);
        int status;
        struct sockaddr_in server;
        status = socket(AF_INET, SOCK_STREAM, 0);
        if ( status < 0){
            perror("Cannot create the socket");
            exit(1);
        }
        server.sin_family = AF_INET;
        server.sin_addr.s_addr = inet_addr("127.0.0.1");
        server.sin_port = htons(1234);
        if ( connect(status, (struct sockaddr*) &server, sizeof(server)) < 0 ){
            perror("Problem connecting");
            exit(1);
        }
        char buf[4] = "\xde\xad\xbe\xef";
        write(status,buf,4);
        close(status);

      }











}
