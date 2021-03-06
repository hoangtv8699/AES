import pyaes
import os


def random(size=16):
    rand = os.urandom(size)
    return rand


class AES:
    rounds_by_key_size = {16: 10, 24: 12, 32: 14}

    def __init__(self, key, iv):
        assert len(key) in AES.rounds_by_key_size
        self.iv = [iv[i] for i in range(len(iv))]
        self.aes = pyaes.AES(key)

    def inc_bytes(self, nonce):
        inc = nonce

        for i in range(len(nonce) - 1, 0, -1):
            if inc[i] == 0xFF:
                inc[i] = 0
            else:
                inc[i] += 1
                break
        return nonce

    def strxor_bytes(self, a, b):
        if len(a) > len(b):
            return [(x ^ y) for (x, y) in zip(a[:len(b)], b)]
        else:
            return [(x ^ y) for (x, y) in zip(a, b[:len(a)])]

    def PKCS_pad(self, text):
        padding_len = 16 - (len(text) % 16)
        for i in range(padding_len):
            text += chr(padding_len)
        return text

    def PKCS_unpad(self, text):
        padding_len = ord(text[-1])
        assert padding_len > 0
        message, padding = text[:-padding_len], text[-padding_len:]
        assert all(ord(p) == padding_len for p in padding)
        return message

    def split_16bytes(self, message):
        assert len(message) % 16 == 0
        message_16bytes = [message[i:i + 16] for i in range(0, len(message), 16)]
        return message_16bytes

    def split_bytes(self, message):
        message_bytes = []
        for i in range(0, len(message), 16):
            if i < len(message):
                message_bytes.append(message[i:i + 16])
            else:
                message_bytes.append(message[i:len(message) - i + 16])
        return message_bytes

    def encrypt_cbc(self, text):
        iv = self.iv
        text = self.PKCS_pad(text)

        blocks = []
        previous = iv.copy()

        for text_block in self.split_16bytes(text):
            text_block_bytes = [ord(c) for c in text_block]
            block = self.aes.encrypt(self.strxor_bytes(text_block_bytes, previous))
            blocks.extend(block)
            previous = block

        return "".join([chr(blocks[i]) for i in range(len(blocks))])

    def decrypt_cbc(self, cipher):
        iv = self.iv

        blocks = []
        previous = iv.copy()

        for cipher_block in self.split_16bytes(cipher):
            cipher_block_bytes = [ord(c) for c in cipher_block]
            block = self.strxor_bytes(previous, self.aes.decrypt(cipher_block_bytes))
            blocks.extend(block)
            previous = cipher_block_bytes

        return self.PKCS_unpad("".join([chr(blocks[i]) for i in range(len(blocks))]))

    def encrypt_ctr(self, text):
        iv = self.iv
        blocks = []
        nonce = iv.copy()
        for text_block in self.split_bytes(text):
            text_block_bytes = [ord(c) for c in text_block]
            block = self.strxor_bytes(text_block_bytes, self.aes.encrypt(nonce))
            blocks.extend(block)
            nonce = self.inc_bytes(nonce)

        return "".join([chr(blocks[i]) for i in range(len(blocks))])

    def decrypt_ctr(self, cipher):
        return self.encrypt_ctr(cipher)
