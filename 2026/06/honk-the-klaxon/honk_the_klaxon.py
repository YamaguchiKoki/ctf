import os
from functools import reduce
from MIX import PBOX

ROUNDS = 32
BLOCK_SIZE = 32

KEY = os.urandom(BLOCK_SIZE)
FLAG = os.getenv("FLAG", "flag{example_flag}")


def pbox(bs):
    return bytes(reduce(lambda x, y: x ^ y, [bs[rowi] for rowi in row]) for row in PBOX)

def bxor(bs1, bs2):
    return bytes([b1 ^ b2 for b1, b2 in zip(bs1, bs2)])

def encrypt(pt, key):
    for _ in range(ROUNDS):
        pt = bxor(pt, key)
        pt = pbox(pt)
    return pt

CHALLENGE = os.urandom(32)
print(f"CHALLENGE: {encrypt(CHALLENGE, KEY).hex()}")


for i in range(210 * 2):
    inp = input("pt: ")
    if inp != "guess":
        pt = bytes.fromhex(inp)
        assert len(pt) == BLOCK_SIZE
        print(encrypt(pt, KEY).hex())

    else:
        challenge_guess = input("challenge: ")
        if bytes.fromhex(challenge_guess) == CHALLENGE:
            print(f"=== Your score is {i} ===")
            print("flag:", FLAG)
        exit()
