from dataclasses import dataclass
from disk_info import DiskInfo
from typing import BinaryIO

ClusterID = int


@dataclass
class FsEntry:
    entry_cluster: int  # cluster where file entry is located
    entry_index: int  # file entry number in entry_cluster
    clusters_count: int  # number of clusters
    is_directory: bool  # whether entry is directory or file


class DiskAnalyzer:
    def __init__(self):
        self.fs_entry_map = dict[ClusterID, FsEntry]

    def analyze(self): ...

    def add_file(self, start_cl: int, entry_cl: int, entry_id: int, is_dir: bool): ...

    def scan_disk(self, file: BinaryIO, info: DiskInfo): ...
