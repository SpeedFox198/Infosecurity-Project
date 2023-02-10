import os

from argon2 import PasswordHasher
from argon2.exceptions import (InvalidHash, VerificationError,
                               VerifyMismatchError)
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

NONCE_LEN = 12
TAG_LEN = 16
ENCRYPT_KEY = os.environ.get("ENCRYPT_KEY", "c0b726dc8240f3f30752abdabd8caf50d77ed51c3aefd4e6d8cea024764894b5")
KEY = bytes.fromhex(ENCRYPT_KEY)

ph = PasswordHasher()

""" Argon Hashing algorithm """


def pw_hash(pw: str | bytes) -> str:
    """ Returns a hashed password """
    return ph.hash(pw)


def pw_verify(hashed: str | bytes,
              pw: str | bytes) -> bool:
    """ Returns True if password is valid """
    try:
        ph.verify(hashed, pw)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False

    return True


def pw_rehash(hashed, pw):
    """ Rehashes a password """
    if ph.check_needs_rehash(hashed):
        return ph.hash(pw)



def encrypt(data: bytes) -> bytes:
    """ Encrypts data using AES in GCM mode """
    nonce = get_random_bytes(NONCE_LEN)

    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)

    ciphertext, tag = cipher.encrypt_and_digest(data)  # write encrypted data below the nonce

    return b"".join([nonce, ciphertext, tag])


def decrypt(data: bytes) -> bytes | None:
    """ Decrypts data using AES in GCM mode """

    # read nonce and generate cipher
    nonce = data[:NONCE_LEN]
    ciphertext = data[NONCE_LEN:-TAG_LEN]
    tag = data[-TAG_LEN:]

    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
    try:
        return cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        return None
