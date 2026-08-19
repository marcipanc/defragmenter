from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BPB:
    """The class implements BPB data structure.
    It includes field common to FAT12, FAT16 and FAT32"""

    BS_jmpBoot: int
    BS_OEMName: str
    BPB_BytsPerSec: int
    BPB_SecPerClus: int
    BPB_RsvdSecCnt: int
    BPB_NumFATs: int
    BPB_RootEntCnt: int
    BPB_ToSec16: int
    BPB_Media: int
    BPB_FATSz16: int
    BPB_SecPerTrk: int
    BPB_NumHeads: int
    BPB_HiddSec: int
    BPB_ToSec32: int


@dataclass(slots=True, frozen=True)
class FAT1216_BPB(BPB):
    """The class implements BPB data structure for FAT12 and FAT16"""

    BPB_DrvNum: int
    BPB_Reserved1: int
    BS_BootSig: int
    BS_BolID: int
    BS_VolLab: str
    BS_FilSysType: str


@dataclass(slots=True, frozen=True)
class FAT32_BPB(BPB):
    """The class implements BPB data structure for FAT32"""

    BPB_FATSz32: int
    BPB_ExtFlags: int
    BPB_FSVer: int
    BPB_RootClus: int
    BPB_FSInfo: int
    BPB_BkBootSec: int
    BPB_Reserved: int
    BS_DrvNum: int
    BS_Reserved1: int
    BS_BootSig: int
    BS_VolID: int
    BS_VolLab: str
    BS_FilSysType: str
