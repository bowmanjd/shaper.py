import base64

from nacl import pwhash
from nacl import secret
from nacl import utils

OPS = pwhash.argon2i.OPSLIMIT_MODERATE
MEM = pwhash.argon2i.MEMLIMIT_MODERATE
kdf = pwhash.argon2i.kdf


def encrypt(password: str, plaintext: str) -> bytes:
    salt = utils.random(pwhash.argon2i.SALTBYTES)

    key = kdf(
        secret.SecretBox.KEY_SIZE, password.encode(), salt, opslimit=OPS, memlimit=MEM
    )
    box = secret.SecretBox(key)
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    ciphertext = box.encrypt(plaintext.encode(), nonce)
    return base64.b64encode(salt + ciphertext)


def decrypt(password: str, ciphertext: bytes) -> str:
    payload = base64.b64decode(ciphertext)
    salt, cipherbytes = (
        payload[: pwhash.argon2i.SALTBYTES],
        payload[pwhash.argon2i.SALTBYTES :],
    )
    key = kdf(
        secret.SecretBox.KEY_SIZE, password.encode(), salt, opslimit=OPS, memlimit=MEM
    )
    box = secret.SecretBox(key)
    received = box.decrypt(cipherbytes)
    return received.decode()
