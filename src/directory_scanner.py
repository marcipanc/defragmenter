from typing import BinaryIO
from models import FsEntry, FsEntryTable, DiskInfo
from constants import ENTRY_SIZE

class DirectoryScanner:
    def __init__(self, stream: BinaryIO, disk_info: DiskInfo):
        self.stream = stream
        self.disk_info = disk_info
        self._entries_per_cluster = disk_info.sec_per_clus \
                        * disk_info.bytes_per_sec // ENTRY_SIZE


    def scan(self) -> FsEntryTable:
        table = FsEntryTable()

        stack: list[tuple[int, int]] = [self.disk_info.]
        

        self.disk_info

    def _calculate_cluster_o
