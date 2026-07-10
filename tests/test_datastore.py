# -*- coding: UTF-8 -*-
import pytest

from russiannames.datastore import NamesDatastore
from russiannames.processor import NamesProcessor


@pytest.fixture(scope="module")
def store():
    return NamesDatastore()


def test_find_existing_record(store):
    record = store.find_one("names", "Николай")
    assert record is not None
    assert record["text"] == "Николай"
    assert "count" in record
    assert record["gender"] in {"m", "f", "u"}
    assert isinstance(record.get("ethnic", []), list)


def test_find_missing_record(store):
    assert store.find_one("names", "Несуществующееимя") is None


def test_lookup_is_injection_safe(store):
    # A value with quotes must not raise or leak into the SQL text.
    assert store.find_one("names", "О'Брайен\"; DROP TABLE names;--") is None


def test_unknown_dataset_raises(store):
    with pytest.raises(ValueError):
        store.find_one("unknown", "x")


def test_rebuilt_datasets_are_consumable(tmp_path):
    tsv_dir = tmp_path / "tsv"
    out_dir = tmp_path / "out"
    tsv_dir.mkdir()
    (tsv_dir / "names.tsv").write_text("Иван\t100\nОльга\t50\n", encoding="utf-8")
    (tsv_dir / "surnames.tsv").write_text("Иванов\t80\nПетросян\t30\n", encoding="utf-8")
    (tsv_dir / "midnames.tsv").write_text("Иванович\t70\nИвановна\t60\n", encoding="utf-8")

    NamesProcessor().build_all(str(tsv_dir), str(out_dir))

    store = NamesDatastore(data_dir=str(out_dir))
    assert store.find_one("names", "Иван")["gender"] == "m"
    assert store.find_one("surnames", "Петросян")["ethnic"] == ["arm"]
    assert store.find_one("midnames", "Ивановна")["fname"] == "Иван"
