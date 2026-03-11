import os
import shutil
import datetime
import tarfile
from backend.core.config import settings

def backup_data():
    """Backup the SQLite database and archived raw files into a single compressed tarball."""
    print("Starting backup process...")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(settings.DATA_DIR, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_filename = f"nexus_sports_backup_{timestamp}.tar.gz"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    archive_dir = settings.ARCHIVE_DIR
    
    with tarfile.open(backup_path, "w:gz") as tar:
        if os.path.exists(db_path):
            print(f"Adding database {db_path} to backup...")
            # Ideally we'd lock or use sqlite backup API, but simple physical copy works for MVP
            tar.add(db_path, arcname="nexus_sports.db")
        else:
            print(f"Warning: Database {db_path} not found.")
            
        if os.path.exists(archive_dir):
            print(f"Adding archived raw files {archive_dir} to backup...")
            tar.add(archive_dir, arcname="archived_files")
            
    print(f"Backup completed successfully: {backup_path}")
    print(f"Size: {os.path.getsize(backup_path) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    backup_data()
