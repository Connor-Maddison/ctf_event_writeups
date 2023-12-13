# Wow | *Misc / Python*

## The task
![task description](/ping_ctf_2023/wow/imgs/task_desc.png)

The task was to beat the challenger in this wow random dice rolling game.

## The process

We started by analysing the provided python file:

```python
FLAG = os.getenv("FLAG", "ping{FAKE}")

random.seed(random.randint(1, 10000000))

[...]

def roll(n: int):
    return random.randint(1, n)

def roll_number(n: int, user: str = "user"):
    if user == "user":
        user = "opponent"
    else:
        user = "user"

    if n == 1:
        return user
    else:
        number = roll(n)
        print(f"{user} rolls {number}")
        return roll_number(number, user)
```

By looking through the code it is clear that the roll utilises standard python random numbers and helpfully for us we know that the seed is determined by a random number between 1 - 10000000.

Therefore if we want to crack this we can just run every possible seed and see which one the script is using.

### The Reverse Script
To do this we start creating a [revese script](/ping_ctf_2023/wow/Task_files/random_exploit.py)

To start we need to connect to the machine and make low bets to figure out the rolls.
![info gathering with low bets](/ping_ctf_2023/wow/imgs/Info_Gathering.png)

Now we know what the rolls are so we can add them to a python array (**note: A quirk of how I coded this to best utilise my time means we need to include the starting roll of 100 before each of the rolls**) Also be sure to keep the tab open as a new seed is created on each connection.

```python
rolls = [100,3,1,100,76,48,18,10,1,100,84,20,17,6,2,2,1,100,5,4,2,1,100,9,4,2,1]
```

Now we just need some code that trys each seed and runs the rolls to see if they match the order of the gathered rolls and if it does it returns us the seed value.

```python
def Main():
    new_seed = 0
    random.seed(new_seed)   ## Set the new seed from 0 - 1000000
    while(True):         

            
        for index, roll in enumerate(rolls):
           
            if index+1 >= len(rolls):
                print(f"ENDED {new_seed}")  ## If we reach the end of our gathered info then thats our seed
                quit()

            if roll == 1:
                print("jump")   ## When reaching the end of a block reset for next one
                continue
            
            real_roll = random.randint(1, roll) ## Random roll the same way as the main code
            print(f"{new_seed} : [{real_roll}] == [{rolls[index+1]}]")
            if real_roll != rolls[index+1]:
                break
        
        new_seed += 1 
        if new_seed > 10000000:
            print("Expended all options : something must be wrong with inputs")
            quit()
        random.seed(new_seed)
```
![Crack the seed](/ping_ctf_2023/wow/imgs/Crack_seed.png)

Now we know the seed for our role is 8499442 it's really simple to change our copy of the code so the see seed to be this value instead of a random value and run them side by side. as we do this we can run our version by betting low values and see if we win or lose. If we win, we bet max on the live version, if we lose we bet low. We keep doing this untill we win and get the flag.
![Side by side](/ping_ctf_2023/wow/imgs/Side_by_Side.png)

<details>
  <summary>Solution / Answer</summary>

![screenshot of flag](/ping_ctf_2023/wow/imgs/Flag.png)

</details>