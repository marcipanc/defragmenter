from typing import BinaryIO
from dataclasses import dataclass
from src.constants import BYTE_ORDER, ClusterID


@dataclass
class DiskInfo:
    """The class implements struct for valuable info about disk file system"""

    bytes_per_sec: int  # Count of bytes per one sector
    sec_per_clus: int  # Count of sectors per one cluster
    fat_start_sector: int  # First sector of FAT table
    fat_size_sectors: int  # Size of FAT table
    num_fats: int  # Number of FAT tables
    first_data_sector: int  # First sector of data
    root_start_sector: int  # First sector of root dir for FAT12/16
    root_clus: int  # Root dir cluster for FAT32
    fat_type: str  # Type of file system

    @classmethod
    def parse_boot_sector(cls, sector_0: bytes) -> "DiskInfo":
        bps = int.from_bytes(sector_0[11:13], BYTE_ORDER)
        spc = sector_0[13]
        rsvd = int.from_bytes(sector_0[14:16], BYTE_ORDER)
        fats = sector_0[16]
        root_ents = int.from_bytes(sector_0[17:19], BYTE_ORDER)
        ts16 = int.from_bytes(sector_0[19:21], BYTE_ORDER)
        fsz16 = int.from_bytes(sector_0[22:24], BYTE_ORDER)
        ts32 = int.from_bytes(sector_0[32:36], BYTE_ORDER)

        if fsz16 != 0:
            fat_sz = fsz16
        else:
            fat_sz = int.from_bytes(sector_0[36:40], BYTE_ORDER)

        fat_start = rsvd
        root_dir_sectors = ((root_ents * 32) + (bps - 1)) // bps
        root_start = fat_start + (fats * fat_sz)
        first_data = root_start + root_dir_sectors
        tot_sec = ts16 or ts32
        data_sec = tot_sec - (rsvd + (fats * fat_sz) + root_dir_sectors)

        total_clusters = data_sec // spc
        root_clus = int.from_bytes(sector_0[44:48], BYTE_ORDER)

        if total_clusters < 4085:
            fat_type = "FAT12"
        elif total_clusters < 65625:
            fat_type = "FAT16"
        else:
            fat_type = "FAT32"

        if fat_type != "FAT32":
            root_clus = -1

        return cls(
            bytes_per_sec=bps,
            sec_per_clus=spc,
            fat_start_sector=fat_start,
            fat_size_sectors=fat_sz,
            num_fats=fats,
            first_data_sector=first_data,
            root_start_sector=root_start,
            root_clus=root_clus,
            fat_type=fat_type,
        )


@dataclass
class FsEntry:
    start_cluster: ClusterID  # number of first cluster
    entry_cluster: ClusterID  # cluster where file entry is located
    entry_index: int  # file entry number in entry_cluster
    clusters_count: int  # number of clusters
    is_directory: bool  # whether entry is directory or file


class FsEntryTable:
    def __init__(self):
        self._entries: dict[int, FsEntry] = {}

    def add(self, entry: FsEntry):
        self._entries[entry.start_cluster] = entry

    def get(self, id: ClusterID) -> FsEntry:
        try:
            return self._entries[id]
        except KeyError:
            raise ValueError(f"Cluster {id} was not found in the table")

    def contains_start_cluster(self, id: ClusterID) -> bool:
        return id in self._entries

    def update_start_cluster(self, old: ClusterID, new: ClusterID):
        try:
            entry = self._entries.pop(old)
            entry.start_cluster = new
            self._entries[new] = entry
        except KeyError:
            raise ValueError(f"Old cluster {old} was not present in the table")

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, id: ClusterID) -> bool:
        return id in self._entries
