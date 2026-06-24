import os
from Crypto.Util.number import getRandomNBitInteger, isPrime, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

flag = os.getenv("FLAG", "Alpaca{REDACTED}").encode()

# experimental 512-bit MODP DH Group like RFC 3526
g = 2
p_hex = """
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08 8A67CC74
020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3CB093 FFFFFFFF FFFFFFFF
"""
p = int.from_bytes(bytes.fromhex(p_hex), "big")
assert p.bit_length() == 512 and isPrime(p)

# order of g is (p - 1) // 2
assert p % 6 == 1 and isPrime((p - 1) // 6)  # p - 1 = 2 * 3 * q
assert pow(g, (p - 1) // 6, p) != 1
assert pow(g, (p - 1) // 3, p) != 1
assert pow(g, (p - 1) // 2, p) == 1


def main():
    a = getRandomNBitInteger(256)

    print("ga = {pow(g, a, p)}")

    gb = int(input("gb = "))

    if not 1 < gb < p - 1:
        raise ValueError("Invalid gb value")

    # 
    # g^b
    flag_enc = encrypt(pow(gb, a, p), flag)
    print(f"flag_enc = {flag_enc.hex()}")


def hash_int(x: int) -> bytes:
    x_bytes = long_to_bytes(x)
    return SHA256.new(x_bytes).digest()


def encrypt(key: int, plaintext: bytes) -> bytes:
    cipher = AES.new(key=hash_int(key), mode=AES.MODE_CBC)
    payload = pad(plaintext, AES.block_size)
    return cipher.iv + cipher.encrypt(payload)


def decrypt(key: int, data: bytes) -> bytes:
    iv, ciphertext = data[: AES.block_size], data[AES.block_size :]
    cipher = AES.new(key=hash_int(key), mode=AES.MODE_CBC, iv=iv)
    payload = cipher.decrypt(ciphertext)
    return unpad(payload, AES.block_size)


if __name__ == "__main__":
    main()
