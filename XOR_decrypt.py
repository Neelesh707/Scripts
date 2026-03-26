import string
import base64

# 62 possible characters (A-Z + a-z + 0-9)
charset = string.ascii_letters + string.digits

def xor_decrypt(data: bytes, key: str) -> bytes:
    key_bytes = key.encode()
    result = bytearray()

    for i in range(len(data)):
        result.append(data[i] ^ key_bytes[i % len(key_bytes)])

    return bytes(result)


# ==========================
# PUT YOUR ENCRYPTED TEXT HERE
# ==========================

# Option 1: If your encrypted text is in HEX
#encrypted_hex = "PASTE_HEX_HERE"

# Option 2: If your encrypted text is Base64, use this instead
encrypted_base64 = "BiA8RSIrPhE4JjFULzA1VC9lP145ZS1eJiorQyQyeVA/ZWoRGwh3EQgqN1cuNzxfKCB5QyQqNBEJaw=="

# Decode the encrypted data
try:
    encrypted_data = bytes.fromhex(encrypted_hex)
except:
    encrypted_data = base64.b64decode(encrypted_base64)


# ==========================
# BRUTE FORCE LAST CHARACTER
# ==========================

for ch in charset:
    key = "KEY_" + ch
    decrypted = xor_decrypt(encrypted_data, key)

    try:
        text = decrypted.decode("utf-8")
        # print only readable text
        if all(32 <= ord(c) < 127 for c in text):
            print(f"[+] KEY FOUND?: {key}  --->  {text}")
    except:
        pass
