from typing import Dict
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from base64 import b64encode, b64decode
import json


def encipher(data: Dict) -> Dict:
    """
    Argument: Dict
    Return:
    msg = {
        "password" : bytes,
        "ciphertext" : Base64 encoded bytes-like object,
        "tag" : bytes,
        "nonce" : cipher.nonce
    }
    """
    # Convert to JSON format
    json_data = json.dumps(data)

    # Generate a password to use for encryption
    password = get_random_bytes(16)

    print('Encrypting data...')
    # Encrypt data
    cipher = AES.new(password, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(json_data.encode())
    print('Done!')

    msg = {
        "password": password,
        "ciphertext": b64encode(ciphertext),
        "tag": tag,
        "nonce": cipher.nonce
    }
    return msg


def decipher(ciphertext: 'b64encoded bytes-like object',
             password: bytes, nonce: bytes, tag: bytes) -> Dict:
    """
    Argument:
    Return:
    Dict like msg
    """
    encrypted_data = b64decode(ciphertext)

    print('Decrypting data...')
    # Decrypt data
    decipher = AES.new(password, AES.MODE_EAX, nonce)
    json_data = decipher.decrypt_and_verify(encrypted_data, tag)

    # Convert JSON string to python dict object
    msg = json.loads(json_data)
    return msg
