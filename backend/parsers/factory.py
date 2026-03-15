import os
import zipfile
from backend.parsers.base import BaseParser
from backend.parsers.fit_gpx import FitGpxParser
from backend.parsers.huawei import HuaweiParser
from backend.parsers.zip_batch import ZipBatchParser


class ParserFactory:
    @staticmethod
    def get_parser(file_path: str) -> BaseParser:
        filename = os.path.basename(file_path).lower()
        ext = os.path.splitext(filename)[1]

        if ext in ['.fit', '.gpx']:
            # Generic FIT/GPX parser
            return FitGpxParser()

        if ext == '.zip':
            # Check if it looks like Huawei
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, 'r') as z:
                    filenames = z.namelist()
                    # Huawei Health export signature
                    if any("MotionPathDetail" in f for f in filenames):
                        return HuaweiParser()
                
                # If it's a ZIP but not Huawei, treat as a batch of sports files
                return ZipBatchParser()

        raise ValueError(f"No parser available for extension {ext}")
