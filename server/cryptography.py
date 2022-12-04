from argon2 import PasswordHasher
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes



KEY = b"NEqIjI1CsQfKQjJXITyC6tLOj_to_YOx-005CMwibVk="
ph = PasswordHasher()


""" Argon Hashing algorithm """
def pw_hash(pw):
    """ Returns a hashed password """
    return ph.hash(pw)


def pw_verify(hashed, pw):
    """ Returns True if password is valid """
    try:
        ph.verify(hashed, pw)
    except:
        return False

    return True


def pw_rehash(hashed, pw):
    """ Rehashes a password """
    if ph.check_needs_rehash(hashed):
        return ph.hash(pw)


""" AES Encryption """
def encrypt(key, data, header):
    """ Encrypts data with AES """
    cipher = AES.new(key, AES.MODE_GCM)
    cipher.update(header)

    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce
    return nonce, tag, ciphertext

def decrypt(key, data, header, nonce, tag):
    """ Decrypts data with AES """
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(header)

    plaintext = cipher.decrypt_and_verify(data, tag)
    return plaintext