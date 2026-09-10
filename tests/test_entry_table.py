import pytest
from src.models import FsEntry, FsEntryTable


@pytest.fixture
def sample_entry() -> FsEntry:
    return FsEntry(
        start_cluster=2,
        entry_cluster=0,
        entry_index=0,
        clusters_count=3,
        is_directory=False,
    )


class TestFsEntryTable:
    def test_initializes_correctly(self):
        table = FsEntryTable()
        assert isinstance(table._entries, dict)

    def test_add_get_entry(self, sample_entry):
        table = FsEntryTable()
        table.add(sample_entry)
        got_entry = table.get(sample_entry.start_cluster)
        assert sample_entry == got_entry

    def test_contains_start_cluster(self, sample_entry):
        table = FsEntryTable()
        table.add(sample_entry)
        assert table.contains_start_cluster(sample_entry.start_cluster)

    def test_update_start_cluster(self, sample_entry):
        table = FsEntryTable()
        table.add(sample_entry)
        old_value = sample_entry.start_cluster
        new_value = 10
        table.update_start_cluster(sample_entry.start_cluster, new_value)
        assert sample_entry.start_cluster == new_value and old_value not in table
        assert new_value in table and table.get(new_value) == sample_entry

    def test_returns_correct_lenght(self, sample_entry):
        table = FsEntryTable()
        assert len(table) == 0
        table.add(sample_entry)
        assert len(table) == 1
        new_entry = FsEntry(3, 0, 0, 3, False)
        table.add(new_entry)
        assert len(table) == 2

    def test_contains_entry(self, sample_entry):
        table = FsEntryTable()
        assert sample_entry.start_cluster not in table
        table.add(sample_entry)
        assert sample_entry.start_cluster in table
