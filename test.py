import attt_aes
import os


# 16 byte block of plain text
plaintext = "Hello World!!!!!"
plaintext_bytes = [ord(c) for c in plaintext]
iv = b'initializationVe'

# 32 byte key (256 bit)
key = b'This_key_for_dem'

# Our AES instance
aes = attt_aes.AES(key, attt_aes.random())

ciphertext = aes.encrypt_ctr(plaintext)
print(ciphertext)
deccript = aes.decrypt_ctr(ciphertext)
print(deccript)