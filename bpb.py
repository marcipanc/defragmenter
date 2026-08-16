from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BPB:
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
class ExtendedFields:
    drv_num: int
    reserved_1: int
    boot_sig: int
    vol_id: int
    vol_lab: str
    fil_sys_type: str


@dataclass(slots=True, frozen=True)
class BPB_12_16(BPB, ExtendedFields):
    pass


@dataclass(slots=True, frozen=True)
class BPB_32(BPB, ExtendedFields):
    fats_z32: int
    ext_flags: int
    fs_ver: int
    root_clus: int
    fs_info: int
    bk_boot_sec: int
    reserved: int
