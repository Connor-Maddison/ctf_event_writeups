import random
import datetime  
import base64

from Crypto.Cipher import AES

iv = b"\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"

decode = base64.b64decode("lQbbaZbwTCzzy73Q+0sRVViU27WrwvGoOzPv66lpqOWQLSXF9M8n24PE5y4K2T6Y")
base_time = datetime.datetime(2023,8,2,10,27,0,0)

for hour_step in range(-13,13):
    utc = base_time + datetime.timedelta(hours=hour_step)

    for sec_step in range(0,60):
        
        tick = utc + datetime.timedelta(seconds=sec_step)

        for milli in range(0,1000):
            fine = tick + datetime.timedelta(milliseconds=milli)
            epoch_time = (fine - datetime.datetime(1970, 1, 1)).total_seconds()
            

            seed = round(epoch_time*1000)
            random.seed(seed)


            key = []
            for i in range(0,16):
                key.append(random.randint(0,255))

            key = bytearray(key)


            cipher = AES.new(key, AES.MODE_CBC, iv) 
            decrypt = cipher.decrypt(decode)
            if b"flag{" in decrypt:
                print(decrypt)
                exit()

