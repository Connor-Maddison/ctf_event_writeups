# Wow | *Misc / Python*

## The task
![task description](/ping_ctf_2023/private-convo/imgs/Task.png)

The task involves deciphering a text file.

## The process

Since we want to decipher the provided text I chose to use python to do that so lets set up our [decipher file.](/ping_ctf_2023/private-convo/task_files/translate.py)

```python 
comment = "xdXdxdXDxDXdXdxDxDXdXDXdxDXdxdXDxDXdXDxdxDXDxDxDxDXdxDxdxDXdxDxDxdXdxdxdxdXDXDxdxDXDxdXDxDXDxDxdxDXdxDxdxDXdXdxDxDXdXDXDxdXdXDXdxDXdXdxdxdXDXDXdxdxdXdXdxDXdXdxDxDXdXDXdxDXDxDxdxdXdxdxdxDXdXDxDxDXdxdx[...]DXdXD"

binary = ""

for char in comment:
    if char.isupper():
        binary += "1"
    else:
        binary += "0"
    


binary_convert = int(binary,2)
byte_num = binary_convert.bit_length() + 7 // 8
binary_array = binary_convert.to_bytes(byte_num, "big")
ascii = binary_array.decode()
print(ascii)


```
This is rather simple, by looking at the comment its clearly a binary reperesentation, You may originally think x = 0, d = 1 but a little bit of closer inspection you will see that is always xd,xd,xd so that doesn't work. Instead we go with capital letters vs lowercase.

This code simply replaces capital letters with a 1 and then lowercase with a 0. It then converts it from binary to ascii.

This gives us:

```
#include <stdio.h>
int main() { int o_983add0ed98b556d85ef118183b229dc[] = { 112, 105, 110, 103, 123, 119, 104, 121, 95, 115, 111, 95, 115, 101, 114, 105, 111, 117, 115, 95, 88, 68, 125 }; const int o_1c1a387bd28e94ce019fcdce8bc08e93 = sizeof((o_983add0ed98b556d85ef118183b229dc)) / sizeof((o_983add0ed98b556d85ef118183b229dc[(0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00)])); char o_7645f9e4a84a7e9f0748c6000a041980[o_1c1a387bd28e94ce019fcdce8bc08e93]; for (int o_f8cd493a89f94a8b1e2e211842b4c8ec = (0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00); (o_f8cd493a89f94a8b1e2e211842b4c8ec < o_1c1a387bd28e94ce019fcdce8bc08e93) & !!(o_f8cd493a89f94a8b1e2e211842b4c8ec < o_1c1a387bd28e94ce019fcdce8bc08e93); ++o_f8cd493a89f94a8b1e2e211842b4c8ec) { o_7645f9e4a84a7e9f0748c6000a041980[o_f8cd493a89f94a8b1e2e211842b4c8ec] = (char)(o_983add0ed98b556d85ef118183b229dc[o_f8cd493a89f94a8b1e2e211842b4c8ec]); }; for (int o_54314e02607d2bca7f2adf644eae54cf = (0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00); (o_54314e02607d2bca7f2adf644eae54cf < o_1c1a387bd28e94ce019fcdce8bc08e93) & !!(o_54314e02607d2bca7f2adf644eae54cf < o_1c1a387bd28e94ce019fcdce8bc08e93); ++o_54314e02607d2bca7f2adf644eae54cf) { putchar(o_7645f9e4a84a7e9f0748c6000a041980[o_54314e02607d2bca7f2adf644eae54cf]); }; putchar('\n'); return (0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00); }; 
```

If you know a bit of C you may recognise the `include <stdio.h>` so from here I created a c file with this code, compiled it and ran it resulting in the flag.

<details>
  <summary>Solution / Answer</summary>

![screenshot of flag](/ping_ctf_2023/private-convo/imgs/flag.png)

</details>