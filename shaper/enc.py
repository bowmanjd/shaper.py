from nacl import pwhash, secret, utils

OPS = pwhash.argon2i.OPSLIMIT_MODERATE
MEM = pwhash.argon2i.MEMLIMIT_MODERATE

def encrypt(password: str, plaintext: str) -> bytes:
    kdf = pwhash.argon2i.kdf
    salt = utils.random(pwhash.argon2i.SALTBYTES)

    key = kdf(secret.SecretBox.KEY_SIZE, password.encode(), salt,
                 opslimit=OPS, memlimit=MEM)
    box = secret.SecretBox(key)
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    ciphertext = box.encrypt(plaintext.encode(), nonce)
    return salt + ciphertext

def decrypt(password: str, ciphertext: bytes) -> str:
    key = kdf(secret.SecretBox.KEY_SIZE, password.encode(), salt,
               opslimit=ops, memlimit=mem)
Bobs_box = secret.SecretBox(Bobs_key)
received = Bobs_box.decrypt(encrypted)
print(received.decode('utf-8'))

