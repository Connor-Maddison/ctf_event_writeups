# PseudoRandom | *Crypto*

## The task
For this task you were supplied with a python file that encrypted a message alongside a result : 

`
Flag Encrypted on 2023-08-02 10:27
lQbbaZbwTCzzy73Q+0sRVViU27WrwvGoOzPv66lpqOWQLSXF9M8n24PE5y4K2T6Y
`

The task was to simply decrypt the hash

## The process
First I extracted parts of the script provided that seemed important, working backwards.
```
cipher = AES.new(key, AES.MODE_CBC, iv) 
ciphertext = cipher.encrypt(flag)

print(base64.b64encode(ciphertext).decode('utf-8'))
```
To start we see that it uses AES encryption with a key, a known iv and then base64 encodes it.
```
key = []
for i in range(0,16):
    key.append(random.randint(0,255))

key = bytearray(key)
```
We can then look at the logic on how the encryption key was made. It was with random ints so might be hard to recreate...

```
ts = time.time()

print("Flag Encrypted on %s" % datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M'))
seed = round(ts*1000)

random.seed(seed)
```
... unless it was random base off the seed. Now I knew I would need to get the seed to find the key, which was based of the `time.time()`. Luckily for us the task actually gives us that time `2023-08-02 10:27`. So lets use that time to try and find the seed.

## The code
For this I created a [decrypt.py](/tenable_ctf_2023/pseudo_random%20/code/dcrypt.py) file.

I firstly initialise the known values of the hash and the date, making sure to convert back from base64:
```
decode = base64.b64decode("lQbbaZbwTCzzy73Q+0sRVViU27WrwvGoOzPv66lpqOWQLSXF9M8n24PE5y4K2T6Y")
base_time = datetime.datetime(2023,8,2,10,27,0,0)

...
```
notice the 0 seconds and milliseconds. This is because we don't know at the exact seconds or milliseconds it ran but we know it will effect the seed as the file rounds the speed to include milliseconds `seed = round(ts*1000)`. To account for this we need to check every possible second and millisecond:
```
for sec_step in range(0,60):
        
        tick = utc + datetime.timedelta(seconds=sec_step)

        for milli in range(0,1000):
            fine = tick + datetime.timedelta(milliseconds=milli)
            epoch_time = (fine - datetime.datetime(1970, 1, 1)).total_seconds()

...
```
notice we also convert to epoch_time as by default datetime will return 2023-08-02 10:27:00 but time.time() is in epoch. Next we simply copy the same code used to encrypt to create a key within the millisecond loop:
```
seed = round(epoch_time*1000)
random.seed(seed)


key = []
for i in range(0,16):
    key.append(random.randint(0,255))

key = bytearray(key)


cipher = AES.new(key, AES.MODE_CBC, iv) 
decrypt = cipher.decrypt(decode)

...
```
Finally we just listen out for the known format of the flag:
```
if b"flag{" in decrypt:
    print(decrypt)
    exit()
```
easy right... Well not quite... When running this you will find that you get no responce, That is because we presumed it was using UTC time, however it is not so we need to account for whatever timezone the target person was in. This isn't too difficult however as all you need to do is add a loop before you adjust the seconds and milliseconds which accounts for -13 -> +13 hours from UTC:
```
for hour_step in range(-13,13):
    utc = base_time + datetime.timedelta(hours=hour_step)

    for sec_step in range(0,60):
        ...
```
And thats it. You should get the flag: `b'flag{r3411y_R4nd0m_15_R3ally_iMp0r7ant}\x00\x00\x00\x00\x00\x00\x00\x00\x00'` A bit messy perhaps and I could have decoded and removed the \x00 but its not necessary. 

### [You can find the full decrypt.py code here](/tenable_ctf_2023/pseudo_random%20/code/dcrypt.py)