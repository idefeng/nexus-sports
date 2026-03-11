import os
import shutil
from typing import Optional
from backend.core.config import settings

def save_uploaded_file(file_bytes: bytes, filename: str) -> str:
    """
    Saves the uploaded raw file to the archive directory for backup.
    Returns the absolute path to the saved file.
    """
    file_path = os.path.join(settings.ARCHIVE_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    return file_path

def delete_archived_file(filepath: str) -> None:
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except OSError:
            pass
