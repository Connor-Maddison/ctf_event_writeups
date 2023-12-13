# Internet Explorer | *Web*

## The task
![task description](/ping_ctf_2023/internet-explorer/imgs/task.png)

The task was to connect to a webpage via internet explorer on linux.

## The process

This task is reletively simple. We start by booting up the web page in burpsuite and connecting to it to gather the get request that is used when connecting. 

Once we have that we can simply google a user agent for internet explorer.
![internet explorer user agent](/ping_ctf_2023/internet-explorer/imgs/user_agent.png)

Now all we have to do is replace the user agent in the get request and replace the `Windows NT` reference with `Linux`

![burpsuite request](/ping_ctf_2023/internet-explorer/imgs/Crafted_Package.png)

And thats it, just send the request and you get the flag.
