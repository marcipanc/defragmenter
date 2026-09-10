from dataclasses import dataclass
from disk_info import DiskInfo
from typing import BinaryIO

ClusterID = int


@dataclass
class FsEntry:
    start_cluster: int  # number of first cluster
    entry_cluster: int  # cluster where file entry is located
    entry_index: int  # file entry number in entry_cluster
    clusters_count: int  # number of clusters
    is_directory: bool  # whether entry is directory or file


class FsEntryTable:
    def __init__(self):
        self._entries: dict[int, FsEntry] = {}

    def add(self, entry: FsEntry):
        self._entries[entry.start_cluster] = entry

    def get(self, cluster: int) -> FsEntry:
        if not self.contains_start_cluster(cluster):
            raise ValueError(f"Cluster {cluster} was not found in the table")
        return self._entries[cluster]

    def contains_start_cluster(self, cluster: int) -> bool:
        return cluster in self._entries

    def update_start_cluster(self, old: int, new: int):
        if old not in self._entries:
            raise ValueError(f"Old cluster {old} was not present in the table")
        entry = self._entries.pop(old)
        entry.start_cluster = new
        self._entries[new] = entry

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, cluster: int) -> bool:
        return cluster in self._entries


class DiskAnalyzer:
    def __init__(self):
        self.fs_entry_map = FsEntryTable()

    def analyze(self): ...

    def add_file(self, start_cl: int, entry_cl: int, entry_id: int, is_dir: bool): ...

    def scan_disk(self, file: BinaryIO, info: DiskInfo): ...
