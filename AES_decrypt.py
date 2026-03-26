#basic AES decryption program that takes a Base64-encoded ciphertext and decrypts it using a hardcoded secret key in ECB mode.

#It:
#Decodes Base64 ciphertext
#Decrypts it using AES (ECB mode)
#Removes padding
#Prints the original plaintext



from Crypto.Cipher import AES
import base64

SECRET_KEY = b'my-secret-key-16'  # must be 16 bytes

encrypted_text = "Nzd42HZGgUIUlpILZRv0jeIXp1WtCErwR+j/w/lnKbmug31opX0BWy+pwK92rkhjwdf94mgHfLtF26X6B3pe2fhHXzIGnnvVruH7683KwvzZ6+QKybFWaedAEtknYkhe"

# Convert from Base64 to bytes
encrypted_data = base64.b64decode(encrypted_text)

cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
decrypted = cipher.decrypt(encrypted_data)

# remove padding
padding_len = decrypted[-1]
decrypted = decrypted[:-padding_len]

print("Decrypted:", decrypted.decode())
