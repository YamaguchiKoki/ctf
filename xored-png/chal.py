import os

key_hex = os.getenv("KEY_HEX", "00112233445566778899aabbccddeeff")
key = bytes.fromhex(key_hex)
assert len(key) == 16

with open("flag.png", "rb") as f_in:
    png = bytearray(f_in.read())

for i in range(len(png)):
    png[i] ^= key[i % len(key)]

with open("flag.png.xored", "wb") as f_out:
    f_out.write(png)

# わかってるー＞暗号化された後のファイル(xored)
# わかりたい→key, 暗号化前(png)
# xored = png ^ key -> png = xored ^ key ->keyが分かればいい
# key[0:15] = png[0:15] ^ xored keyが16桁なので、png[0:15]が分かればいい
