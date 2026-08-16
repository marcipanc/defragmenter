from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BPB:
    """The class implements BPB data structure.
    It includes field common to FAT12, FAT16 and FAT32"""

    jump_boot: int
    oem_name: str
    byts_per_sec: int
    sec_per_clus: int
    rsvd_sec_cnt: int
    num_fats: int
    root_ent_cnt: int
    tot_sec_16: int
    media: int
    fats_z16: int
    sec_per_trk: int
    num_heads: int
    hidd_sec: int
    to_sec_32: int


@dataclass(slots=True, frozen=True)
class BPB_12_16(BPB):
    """The class implements BPB data structure for FAT12 and FAT16"""

    drv_num: int
    reserved_1: int
    boot_sig: int
    vol_id: int
    vol_lab: str
    fil_sys_type: str


@dataclass(slots=True, frozen=True)
class BPB_32(BPB):
    """The class implements BPB data structure for FAT32"""

    fats_z32: int
    ext_flags: int
    fs_ver: int
    root_clus: int
    fs_info: int
    bk_boot_sec: int
    reserved: int
    drv_num: int
    reserved_1: int
    boot_sig: int
    vol_id: int
    vol_lab: str
    fil_sys_type: str
