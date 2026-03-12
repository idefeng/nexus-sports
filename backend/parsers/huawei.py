from typing import List

from backend.parsers.base import BaseParser
from backend.schemas.activity import ActivityCreate


class HuaweiParser(BaseParser):
    """
    Placeholder parser for Huawei Health ZIP exports.
    
    TODO: Implement actual parsing of Huawei JSON schema 
    (reference: Hitrava project for format details).
    """
    
    def parse(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        raise NotImplementedError(
            "华为运动健康数据解析尚未实现。"
            "请使用高驰 FIT/GPX 格式文件导入，或联系开发者添加华为支持。"
        )
