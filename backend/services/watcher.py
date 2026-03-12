import os
import time
import requests
import argparse
import logging
from pathlib import Path

from backend.core.config import settings

logger = logging.getLogger("nexus_sports.watcher")

# Try importing watchdog, if not installed we will poll manually
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    HAS_WATCHDOG = True
except ImportError:
    HAS_WATCHDOG = False
    logger.warning("watchdog package not found. Falling back to simple polling.")

API_URL = settings.BACKEND_API_URL
SUPPORTED_EXTENSIONS = {'.fit', '.gpx', '.zip'}
PROCESSED_FILES = set()

def upload_file(filepath: str):
    """Hits the FastAPI upload endpoint with the new file."""
    path_obj = Path(filepath)
    if path_obj.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return
        
    if str(path_obj.absolute()) in PROCESSED_FILES:
        return
        
    logger.info("Detected new file: %s", path_obj.name)
    
    try:
        # Prevent reading file that is still being written to disk
        time.sleep(2) 
        
        with open(filepath, 'rb') as f:
            files = {'files': (path_obj.name, f, 'application/octet-stream')}
            resp = requests.post(f"{API_URL}/upload", files=files)
            
        if resp.status_code == 200:
            results = resp.json().get('results', [])
            for res in results:
                status = res.get('status')
                msg = res.get('message')
                if status == 'success':
                    logger.info("  -> Successfully imported: %s", msg)
                elif status == 'skipped':
                    logger.info("  -> Skipped (duplicate): %s", msg)
                else:
                    logger.warning("  -> Error parsing: %s", msg)
        else:
            logger.error("  -> Server returned error %d: %s", resp.status_code, resp.text)
            
    except Exception as e:
        logger.error("  -> Failed to upload %s: %s", path_obj.name, e)
        
    finally:
        # Mark as processed regardless of failure to avoid infinite loops
        PROCESSED_FILES.add(str(path_obj.absolute()))

if HAS_WATCHDOG:
    class UploadEventHandler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                upload_file(event.src_path)
                
        def on_modified(self, event):
            if not event.is_directory:
                upload_file(event.src_path)

def start_watcher(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"Created watch directory: {directory}")
        
    print(f"Starting to watch {directory} for fitness files...")
    
    if HAS_WATCHDOG:
        event_handler = UploadEventHandler()
        observer = Observer()
        observer.schedule(event_handler, directory, recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        # Simple Polling fallback
        try:
            while True:
                for file in os.listdir(directory):
                    filepath = os.path.join(directory, file)
                    if os.path.isfile(filepath):
                        upload_file(filepath)
                time.sleep(10)
        except KeyboardInterrupt:
            print("Watcher stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nexus Sports Auto-Import Watcher")
    parser.add_argument("--dir", type=str, default="./data/auto_import", help="Directory to watch")
    args = parser.parse_args()
    
    start_watcher(args.dir)
