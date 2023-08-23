#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<stdlib.h>
int main(){
	/*
	fd[0] 為讀取資料
	fd[1]  為寫入資料

	*/
	int arr[2];
	pipe(arr);
	pid_t child;
	printf("%d\n",child);
	if((child=fork())==0)
	{
		printf("im child\n");
		write(arr[1],"id",sizeof("id"));
		close(arr[0]);//close read
		close(arr[1]);
		printf("child end\n");
		exit(0);
	}
	else{
		printf("im parent\n");

		char buf[30];
		// read(arr[0],buf,sizeof(buf));
		// printf("%s\n",buf );
		dup2(arr[0],0);
		close(arr[0]);
		close(arr[1]);
		printf("parent end\n");

		execve("/bin/bash",NULL,NULL);
	}
}
