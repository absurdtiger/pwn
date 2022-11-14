# All the information I organised here last time is gone. curse you inconsistent saving behaviour

## general pwn notes
GENERAL PAYLOAD: [buffer][addr of function you want to call] 

### basic idea
- function that allows for buffer overflow (overwriting more data than it's supposed to)
- overwrite RIP
- control program and execution
- it's ROP if there are many gadgets
- it's libc if there is libc
- this should be double confirmed

### data formatting
- little endian is just the order in which the hex is presented and read
- p64() is for 64-bit
- p32() for 32-bit
- both p64() and p32() are in Little Endian
- p64() would usually be for 8 byte long addresses
- p32() should be used for data types of size 4 bytes (like integers)
- int(data, base) converts data into the specified base
- addresses can be declared as p64(0xdeadbeef) which would store it as 8-bit bytes
- non-hex strings must be converted into base 16 strings with int(b"string", 16) before being converted to 8-bit
- LiveOverflow uses the `struct` library to convert integers to binary strings

### Addresses
gdb is useful
- `file [binary]` to select a file
- `pattern create 2000` to create de brujin sequence of 2000 digits long
- `r` to run binary
- `pattern search $rbp` to find rbp offset
  - if you can successfully find rbp in little-endian, rip is offset of rbp + 8
- alternatively `info frame` will show you rip and whether it is overwritten
  - there's not really an easy way to find the offset from the overwritten sequence but you can still try
- `info function` finds function addresses but it's a bit of a dump
  - `rabin2 -R [binary]` to find function addresses and PLT addresses faster 
- in the event that gdb is annoying and won't give you the offset use a diff disassembler like IDA or binaryninja
- test altered GOT addresses in gdb by setting breakpoints, and using `set {int} 0xaddrone=0xaddrtwo`
- `set $rax = ` to set registers

### more about registers

- **general purpose registers** are RAX, RBX, RCX, RDX, RDI, RSI, RBP, RSP, R8-15
- **segments** are ES, CS, SS, DS, FS
- **EFLAGS** are CF, PF, AF, ZF, SF,...
- RIP: special _instruction pointer_ and is modified as a side-effect
- RAX: accumulator
- RBX: base
- RCX: counter
- RDX: data/general
- RSI: source index
- RDI: destination index
- RBP: base pointer
- RSP: stack pointer

### dynamic analysis with gdb
- if the program requires code execution and values to be placed on the stack, it would need dynamic analysis to figure out the offset on the stack and stuff
- so yes we need to use gdb attach through pwntools I cannot escape this
```python
from pwn import *
context.log_level='debug'
p = whatever
pid = gdb.attach(p, 'b main')
```

## null-terminating strings (logic bug)
[1 NULL][buffer] <- compare with -> [1 NULL][unknown comparison]

buffer overflow is required to overwrite the second value in the strcmp\n
alternatively, \n
[NULL] <- compare with -> [NULL][unknown string]

# checksec
- stack canary checks if a value on the stack has remained constant. if the function is not the same the program terminates
- NX: NX for non-executable. If you change the return address by an address of the stack where you put some code, you would get a SEGFAULT. So, no shellcode on the stack. Overcome NX by using ret2libc.
- PIE changes the virtual addresses of the program and stops it from being static
  - if PIE is enabled you need to find the base address and calculate the offset from there (similar to ret2libc)
- Full RELRO: RELRO is for Relocation Read-Only. Linux uses ELF binary format. In this binary, functions called by the program from dependent libraries (like printf from libc) are dynamically resolved. The first time the function is called, the address is resolved. If your program has a vulnerability that makes it possible to write somewhere in the memory, you can overwrite such address by your own (or replace the address of printf by the address of the function system).
- partial RELRO: you can write to the GOT table to redirect code execution

## canary
[buffer][canary][buffer][flag function]
- there are a few ways to leak the canary
- Additional example: [string0.py](./Canary/string0.py) for [string0](./Canary/string0)

### format string
- if a printing function takes in user-supplied data. fprintf, printf, sprintf, syslog
- given a format string vulnerability, `%n$p` where n is the pointer offset. `%s` `%x`
- ~~the pointer leaking is probably of the master canary, while the thing you need to keep constant is the local canary~~ Unreliable because "I was high when I said this" :eyeroll: smh
- to find `n`, need to use a brute force script, an example is added under [leak_canary.py](./Canary/leak_canary.py)

### buffer overflow to find canary
- in gdb, `b * <addr of stackcheck>` set breakpoint before canary check
- pattern create/search
- search canary 
- will return the contents of the canary before the program crashes

### IDA
- you can use IDA to find the canary location on the stack, the canary is declared as an unsigned integer, then use the ebp/rbp offset
- you can also use IDA to find the subsequent instruction pointer address (shown as `r` most of the time)
- using gdb would be easier

# ROP

## Finding gadgets
`ROPgadget --binary=<binary> | grep pop, etc`

## ROP to shell
[buffer][ret][write "/bin/sh\x00" into memory][set up calling convention for execve][syscall]
- rdi=filename(pointer to "/bin/sh\x00")
- rsi=0
- rdx=0
- rax=59 in hex(0x3b)
- call syscall

Making a system call to execve("/bin/sh") (or any execve) has requirements for certain registers <https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/>

For a shell, the string "/bin/sh\x00" has to be in the memory somewhere; you can search for the string with either of the following:
```bash
$ rabin2 -z [binary]
$ ROPgadget --binary [binary] --string "/bin/sh\x00"
```
or automate it (only possible with libc)
```python
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
```

## ROP to general function with arguments
`[buffer][ret][necessary writes][changing registers][function]`

certain challenges may require functions to be called without libc, [speedrun](./.archive/speedrun-exploit.py), [write4](../ROPemporium/write4/exploit.py)

==============
- for things like strings, it needs to be written into the memory, which requires some funny pointer magic 

### rop chain to write /bin/sh into memory
- find a `mov qword ptr` gadget
- find a free space in the memory
  - CTRL+C to finish a program without entering any input
  - `vmmap` in gdb
  - `x/8x 0xaddress`
- change the registers in the gadget to reflect the location in the memory and "/bin/sh\x00"

### find /bin/sh in libc
- find string in program with the string "/bin/sh", and libc contains that string
- inspect the memory layout of the program with `info proc map`, and identify where libc starts
- `strings -a -t x /lib/i386-linux-gnu/libc-2.27.so | grep "/bin/sh"` to find the offset of the string
- add the address of libc and "/bin/sh"
- check if the string is at the location with `x/s <addr>`
- or `ROPgadget --binary ./libc.so.6 --strings "/bin/sh"`
=================================
# ret2libc
### Glossary
- GOT: Global Offsets Table
- PLT: Procedure Linkage Table

## Understanding global function execution
- PLT stub -> GOT -> glibc -> PLT extended
- calling the address of GOT would return the address of that actual function in libc

### When GOT writeable
- in the event there is something like an exit() function you need to avoid (which prevents the function from returning therefore there is no rip to overwrite)
- let's say hello() is the function you want to call
- store addr of hello()
- store GOT address of exit() 
- overwrite the address in GOT to hello(). [format string example](https://www.youtube.com/watch?v=t1LH9D5cuK4)

### When GOT unwriteable (NX enabled, PIE enabled, full RELRO)
- for a print function (puts, printf) in libc called in the main program,
- set rdi to the GOT addr
- call the main print function
- collect the libc addr of the print function
- use that to search for the libc
- test with libc using pwntools
- one_gadget sys execve (hardcode)
- send location of the gadget (addr + libc base)
- win
