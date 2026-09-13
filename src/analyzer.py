from dataclasses import dataclass
from disk_info import DiskInfo
from typing import BinaryIO

from src.models import FsEntryTable

class DiskAnalyzer:
    def __init__(self):
        self.fs_entry_map = FsEntryTable()

    def analyze(self): 
        ...

    def add_file(self, start_cl: int, entry_cl: int, entry_id: int, is_dir: bool): 
        fs_entry = FsEntry(start_cl, entry_cl. ent]b)

    def scan_disk(self, file: BinaryIO, info: DiskInfo): 
        ...
