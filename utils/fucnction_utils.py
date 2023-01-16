import hashlib


def encrypt_password(password):
    salt = b''
    encrypted_password = str(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000))
    return encrypted_password
