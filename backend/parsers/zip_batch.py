import os
import zipfile
import tempfile
import shutil
from typing import List
from backend.parsers.base import BaseParser
from backend.schemas.activity import ActivityCreate
from backend.core.config import logger

class ZipBatchParser(BaseParser):
    """
    Parser for general ZIP archives containing multiple FIT or GPX files.
    """

    def parse(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        activities = []
        if not zipfile.is_zipfile(file_path):
            logger.error("Not a valid ZIP file: %s", file_path)
            return activities

        # Create a temporary directory for extraction
        temp_dir = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                z.extractall(temp_dir)
            
            # Late import to avoid circular dependency
            from backend.parsers.factory import ParserFactory
            
            # Recursively walk through the extracted files
            for root, _, files in os.walk(temp_dir):
                for filename in files:
                    sub_file_path = os.path.join(root, filename)
                    ext = os.path.splitext(filename)[1].lower()
                    
                    # Skip non-sport files or nested ZIPs for now to keep it simple
                    if ext in ['.fit', '.gpx']:
                        try:
                            # Calculate a semi-unique hash for the sub-file to keep tracking accurate
                            # For simplicity, we can just use the name + original hash
                            sub_file_hash = f"{original_file_hash}_{filename}"
                            
                            # We don't use ParserFactory here directly to avoid getting another ZipBatchParser
                            # if someone zipped a zip. We just use FitGpxParser for these extensions.
                            from backend.parsers.fit_gpx import FitGpxParser
                            sub_parser = FitGpxParser()
                            
                            logger.info("ZipBatch: Processing sub-file %s", filename)
                            sub_activities = sub_parser.parse(sub_file_path, sub_file_hash)
                            activities.extend(sub_activities)
                        except Exception as e:
                            logger.error("ZipBatch: Error processing %s: %s", filename, e)
                    
                    elif ext == '.zip':
                        # Optional: handle nested Huawei or other ZIPs? 
                        # For now, let's keep it focus on FIT/GPX.
                        pass
        except Exception as e:
            logger.error("ZipBatch: Extraction/Processing error: %s", e)
        finally:
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            
        return activities
