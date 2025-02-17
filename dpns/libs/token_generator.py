import hashlib
import uuid


def hash_md5(text: str):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def generate_token():
    return uuid.uuid4().hex


