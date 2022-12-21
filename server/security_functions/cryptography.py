from argon2 import PasswordHasher
from Crypto.Cipher import AES
import os



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


""" Generate a key and save it into a file """
def generate_key():
    key = os.urandom(32)
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    key_file.close()


data = "sensitive data" # users' data to be encrypted

""" AES Encryption """
#file_out will have 3 lines:
# 1. nonce
# 2. encrypted data
# 3. tag
def encrypt(data:str):
    """ Encrypts data with AES """
    with open('key.key', 'rb') as key_file:
        key = key_file.read()
    key_file.close()

    data_byte = data.encode()

    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce

    ciphertext, tag = cipher.encrypt_and_digest(data_byte) # write encrypted data below the nonce

    result = b''.join([nonce, ciphertext, tag]) # write nonce, encrypted data, and tag

    return result
    

def decrypt(result:bytes):
    """ Decrypts data with AES """

    #read key
    with open('key.key', 'rb') as key_file:
        key = key_file.read()
    key_file.close()

    #read nonce and generate cipher
    nonce = result[:16]
    ciphertext = result[16:-16]
    tag = result[-16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    #decrypt data
    plaintext_bytes = cipher.decrypt_and_verify(ciphertext, tag)
    plaintext = plaintext_bytes.decode()
    
    return plaintext


# Test
# generate_key()
# result = encrypt(data)
# print(result)
# print(decrypt(result))
