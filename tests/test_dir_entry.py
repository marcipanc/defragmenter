import pytest
from src.models import DirEntry


@pytest.fixture
def fat12_entry() -> bytes:
    return b"FILE    TXT \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x02\x00\x00"


@pytest.fixture
def fat16_entry() -> bytes:
    return b"FILE    TXT \x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x10\x00\x10\x00\x00\x00"


@pytest.fixture
def fat32_entry() -> bytes:
    return b"FILE    TXT \x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x05\x00\x00\x00\x01\x00"


@pytest.fixture
def fat32_subdir_entry() -> bytes:
    return b"DOCS       \x10\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00"


@pytest.fixture
def empty_entry() -> bytes:
    return b"\x00" * 32


@pytest.fixture
def deleted_entry() -> bytes:
    return b"\xe5LD_FILETXT \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x10\x00\x00"


@pytest.fixture
def dot_entry() -> bytes:
    return b".          \x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00"


class TestDirEntryCreating:
    def test_fat12_entry(self, fat12_entry):
        entry = DirEntry.from_bytes(fat12_entry)
        assert entry.name == b"FILE    "
        assert entry.ext == b"TXT"
        assert entry.attr == 0x20
        assert entry.first_cluster_high == 0
        assert entry.first_cluster_low == 0x0003
        assert entry.size == 512

    def test_fat16_entry(self, fat16_entry):
        entry = DirEntry.from_bytes(fat16_entry)
        assert entry.name == b"FILE    "
        assert entry.ext == b"TXT"
        assert entry.attr == 0x20
        assert entry.first_cluster_high == 0xFF00
        assert entry.first_cluster_low == 0x0010
        assert entry.size == 16

    def test_fat32_entry(self, fat32_entry):
        entry = DirEntry.from_bytes(fat32_entry)
        assert entry.name == b"FILE    "
        assert entry.ext == b"TXT"
        assert entry.attr == 0x20
        assert entry.first_cluster_high == 0x0002
        assert entry.first_cluster_low == 0x0005
        assert entry.size == 65536

    def test_fat32_dir_entry(self, fat32_subdir_entry):
        entry = DirEntry.from_bytes(fat32_subdir_entry)
        assert entry.name == b"DOCS    "
        assert entry.ext == b"   "
        assert entry.attr == 0x10
        assert entry.first_cluster_high == 0x0002
        assert entry.first_cluster_low == 0x0000
        assert entry.size == 0


class TestDirEntryProperties:
    def test_empty_property(self, empty_entry):
        entry = DirEntry.from_bytes(empty_entry)
        assert entry.is_empty

    def test_deleted_property(self, deleted_entry):
        entry = DirEntry.from_bytes(deleted_entry)
        assert entry.is_deleted

    def test_dot_property(self, dot_entry):
        entry = DirEntry.from_bytes(dot_entry)
        assert entry.is_dot_entry

    def test_dir_property(self, fat32_subdir_entry):
        entry = DirEntry.from_bytes(fat32_subdir_entry)
        assert entry.is_dir

    def test_get_cluster_property_fat32(self, fat32_entry):
        entry = DirEntry.from_bytes(fat32_entry)
        assert entry.get_start_cluster(True) == 131077

    def test_get_cluster_property_fat16(self, fat16_entry):
        entry = DirEntry.from_bytes(fat16_entry)
        assert entry.get_start_cluster(False) == 16
