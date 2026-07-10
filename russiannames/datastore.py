# -*- coding: UTF-8 -*-
"""Embedded DuckDB storage backend for russiannames.

Loads the reference datasets (``names``, ``surnames``, ``midnames``) from Parquet
files into an in-memory DuckDB database and answers exact-match lookups by the
``text`` key. No external database server is required.
"""

import os
from importlib import resources
from typing import Optional

import duckdb

ENV_DATA_DIR = "RUSSIANNAMES_DATA_DIR"
DATASETS = ("names", "surnames", "midnames")


def _bundled_data_dir():
    """Return the directory holding the Parquet datasets shipped with the package."""
    return str(resources.files(__package__).joinpath("data"))


def resolve_data_dir(data_dir=None):
    """Resolve the dataset directory.

    Precedence: explicit ``data_dir`` argument, then the ``RUSSIANNAMES_DATA_DIR``
    environment variable, then the datasets bundled with the installed package.
    """
    if data_dir:
        return str(data_dir)
    env_dir = os.environ.get(ENV_DATA_DIR)
    if env_dir:
        return env_dir
    return _bundled_data_dir()


class NamesDatastore:
    """DuckDB-backed store for exact-match name lookups over Parquet datasets."""

    def __init__(self, data_dir: Optional[str] = None) -> None:
        self.data_dir = resolve_data_dir(data_dir)
        self._conn = duckdb.connect(database=":memory:")
        self._loaded = set()

    def _dataset_path(self, dataset):
        return os.path.join(self.data_dir, "%s.parquet" % dataset)

    def _ensure_loaded(self, dataset):
        if dataset in self._loaded:
            return
        if dataset not in DATASETS:
            raise ValueError("Unknown dataset: %r" % dataset)
        path = self._dataset_path(dataset)
        if not os.path.exists(path):
            raise FileNotFoundError("Dataset parquet not found: %s" % path)
        self._conn.execute(
            "CREATE TABLE %s AS SELECT * FROM read_parquet(?)" % dataset, [path]
        )
        try:
            self._conn.execute(
                "CREATE INDEX idx_%s_text ON %s(text)" % (dataset, dataset)
            )
        except duckdb.Error:
            # Index is a performance optimization; ignore if unsupported.
            pass
        self._loaded.add(dataset)

    def find_one(self, dataset: str, text: str) -> Optional[dict]:
        """Return the first record whose ``text`` equals ``text`` as a dict, or None."""
        self._ensure_loaded(dataset)
        cur = self._conn.execute(
            "SELECT * FROM %s WHERE text = ? LIMIT 1" % dataset, [text]
        )
        row = cur.fetchone()
        if row is None:
            return None
        columns = [d[0] for d in cur.description]
        # Drop NULL-valued columns so the record mirrors the sparse documents the
        # parser expects (it uses ``'gender' in record`` / ``'ethnic' in record``).
        record = {col: val for col, val in zip(columns, row) if val is not None}
        if "ethnic" in record:
            record["ethnic"] = list(record["ethnic"])
        return record

    def close(self):
        self._conn.close()
