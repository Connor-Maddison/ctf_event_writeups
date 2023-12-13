# Inside Bear | *Misc / Stego*

## The task
![task description](/ping_ctf_2023/inside-bear/imgs/task.png)

The task was to extract the flag from a file.

## The process

First we can try running the look-inside file but like can be seen in the provided c file all it does is print "hi mum". 

So the next step I took was to see if this was actually just a normal file. The large file size for such a simple script was imidiatly odd, so I ran some stegography tools including binwalk, and it turns out there was more to the file then it seemed.
![binwalk extracting the file](/ping_ctf_2023/inside-bear/imgs/binwalk.png)

This gave us a gif and 2 sound files, the gif didn't provide anything more neither did the static.ogg (which isn't much fun to listen to either). However the `CAPTURED_TRANSMISSION.wav` not only was an interesting name but had an odd mechanical sound to it. So I started running some audio tools including looking at the soundwaves and didn't get too far. However a bit more poking around and I tested it on [https://morsecode.world/international/decoder/audio-decoder-adaptive.html](https://morsecode.world/international/decoder/audio-decoder-adaptive.html) to see if it happened to be morse code.

![morse code translation](/ping_ctf_2023/inside-bear/imgs/morse_code.png)

Turns out it was and the file output this code which after base64 decoding gave us the flag. 

<details>
  <summary>Solution / Answer</summary>

![screenshot of flag](/ping_ctf_2023/inside-bear/imgs/flag.png)

**Note: The decode is slightly off however context clues allowed the flag to be entered correctly**

</details>