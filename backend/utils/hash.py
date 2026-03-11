import hashlib
import os

def calculate_file_hash(file_path: str, chunk_size: int = 8192) -> str:
    """Calculate the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()

def calculate_bytes_hash(data: bytes) -> str:
    """Calculate MD5 hash of bytes data."""
    return hashlib.md5(data).hexdigest()
