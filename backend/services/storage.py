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

def clear_all_archives() -> None:
    """Removes all files from the archive directory."""
    if os.path.exists(settings.ARCHIVE_DIR):
        for filename in os.listdir(settings.ARCHIVE_DIR):
            file_path = os.path.join(settings.ARCHIVE_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception:
                pass
