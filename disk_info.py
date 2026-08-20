from dataclasses import dataclass

BYTE_ORDER = "little"


@dataclass
class DiskInfo:
    """The class implements struct for valuable info about disk file system"""

    bytes_per_sec: int
    sec_per_clus: int
    fat_start_sector: int
    fat_size_sectors: int
    num_fats: int
    first_data_sector: int
    root_start_sector: int  # FAT12/16
    root_clus: int  # FAT32
    fat_type: str

    @classmethod
    def parse_boot_sector(cls, sector_0: bytes):
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

        return {
            "bytes_per_sec": bps,
            "sec_per_clus": spc,
            "fat_start_sector": fat_start,
            "fat_size_sectors": fat_sz,
            "num_fats": fats,
            "first_data_sector": first_data,
            "root_start_sector": root_start,
            "root_clus": root_clus,
            "fat_type": fat_type,
        }
