from abc import ABC, abstractmethod
from typing import List
from backend.schemas.activity import ActivityCreate

class BaseParser(ABC):
    """Abstract parser base class."""
    
    @abstractmethod
    def parse(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        pass
