# -*- coding: UTF-8 -*-
"""Build the russiannames reference datasets as Parquet files.

This module rebuilds the ``names``, ``surnames`` and ``midnames`` datasets from
frequency TSV files (``text<TAB>count`` produced by :mod:`russiannames.reader`)
and rule-based enrichment. It is fully MongoDB-free: the datasets are written as
Parquet via DuckDB so they can be consumed by :class:`russiannames.datastore`.
"""

import os
import re

import duckdb

from .consts import (
    GENDER_BOTH,
    GENDER_FEMALE,
    GENDER_MALE,
    NAME_POSTFIXES,
    SURN_NATIONAL_RULES,
    SURNAME_POSTRULES,
)

DATASETS = ("names", "surnames", "midnames")

# Parquet schema per dataset (column order matters for INSERT/COPY).
SCHEMAS = {
    "names": [
        ("count", "BIGINT"),
        ("text", "VARCHAR"),
        ("ethnic", "VARCHAR[]"),
        ("lett", "VARCHAR"),
        ("gender", "VARCHAR"),
    ],
    "surnames": [
        ("count", "BIGINT"),
        ("gender", "VARCHAR"),
        ("ethnic", "VARCHAR[]"),
        ("f_form", "VARCHAR"),
        ("fname", "VARCHAR"),
        ("text", "VARCHAR"),
    ],
    "midnames": [
        ("count", "BIGINT"),
        ("gender", "VARCHAR"),
        ("ethnic", "VARCHAR[]"),
        ("lett", "VARCHAR"),
        ("fname", "VARCHAR"),
        ("text", "VARCHAR"),
    ],
}

# Patronymic suffix -> reconstructed first name, used to link midnames to names.
MIDNAME_TO_NAME_RULES = [
    ("инична", lambda s: s[:-4] + "а"),
    ("ьевич", lambda s: s[:-5] + "ий"),
    ("иевич", lambda s: s[:-5] + "ий"),
    ("левич", lambda s: s[:-5] + "ль"),
    ("ревич", lambda s: s[:-5] + "рь"),
    ("еевич", lambda s: s[:-5] + "ей"),
    ("аевич", lambda s: s[:-5] + "ай"),
    ("ьевна", lambda s: s[:-5] + "ий"),
    ("иевна", lambda s: s[:-5] + "ий"),
    ("ревна", lambda s: s[:-5] + "рь"),
    ("левна", lambda s: s[:-5] + "ль"),
    ("еевна", lambda s: s[:-5] + "ей"),
    ("аевна", lambda s: s[:-5] + "ай"),
    ("ович", lambda s: s[:-4]),
    ("овна", lambda s: s[:-4]),
    ("ична", lambda s: s[:-4] + "а"),
]


def guess_by_rules(name, rules):
    """Return the first ``(pattern, value)`` whose pattern matches ``name``."""
    for pattern, value in rules.items():
        if re.match(pattern, name):
            return pattern, value
    return None


def _gender_letter(rule_value):
    if rule_value == GENDER_MALE:
        return "m"
    if rule_value == GENDER_FEMALE:
        return "f"
    return "u"


def recognize_name_gender(name):
    res = guess_by_rules(name, NAME_POSTFIXES)
    return _gender_letter(res[1]) if res else None


def recognize_surname_gender(name):
    res = guess_by_rules(name, SURNAME_POSTRULES)
    if not res or res[1] == GENDER_BOTH:
        return "u" if res else None
    return _gender_letter(res[1])


def recognize_midname_gender(name):
    if len(name) <= 3:
        return "u"
    if name.endswith("ич"):
        return "m"
    if name[-3:] in ("вна", "чна", "шна"):
        return "f"
    if name.endswith("оглы") or name.endswith("Оглы"):
        return "m"
    if name.endswith("кызы") or name.endswith("Кызы"):
        return "f"
    return "u"


def recognize_surname_ethnic(name):
    res = guess_by_rules(name, SURN_NATIONAL_RULES)
    return list(res[1]) if res else None


def midname_to_firstname(name):
    for suffix, transform in MIDNAME_TO_NAME_RULES:
        if name.endswith(suffix):
            return transform(name)
    return None


def read_frequency_tsv(filename):
    """Read a ``text<TAB>count`` TSV into a list of ``(text, count)`` tuples."""
    records = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            text = parts[0].strip()
            if not text:
                continue
            try:
                count = int(parts[1])
            except ValueError:
                continue
            records.append((text, count))
    return records


class NamesProcessor:
    """Rebuild reference datasets into Parquet without any external database."""

    def build_names(self, records):
        rows = []
        for text, count in records:
            rows.append([
                count,
                text,
                None,
                text[0] if text else None,
                recognize_name_gender(text),
            ])
        return rows

    def build_surnames(self, records):
        rows = []
        for text, count in records:
            rows.append([
                count,
                recognize_surname_gender(text),
                recognize_surname_ethnic(text),
                None,
                None,
                text,
            ])
        return rows

    def build_midnames(self, records):
        rows = []
        for text, count in records:
            rows.append([
                count,
                recognize_midname_gender(text),
                None,
                text[0] if text else None,
                midname_to_firstname(text),
                text,
            ])
        return rows

    def write_parquet(self, dataset, rows, out_path):
        schema = SCHEMAS[dataset]
        columns = ", ".join("%s %s" % (name, typ) for name, typ in schema)
        placeholders = ", ".join(["?"] * len(schema))
        conn = duckdb.connect(database=":memory:")
        try:
            conn.execute("CREATE TABLE %s (%s)" % (dataset, columns))
            if rows:
                conn.executemany(
                    "INSERT INTO %s VALUES (%s)" % (dataset, placeholders), rows
                )
            conn.execute(
                "COPY %s TO ? (FORMAT PARQUET)" % dataset, [out_path]
            )
        finally:
            conn.close()

    def build_dataset(self, dataset, tsv_path, out_dir):
        records = read_frequency_tsv(tsv_path)
        builder = getattr(self, "build_%s" % dataset)
        rows = builder(records)
        out_path = os.path.join(out_dir, "%s.parquet" % dataset)
        self.write_parquet(dataset, rows, out_path)
        return out_path

    def build_all(self, tsv_dir, out_dir):
        """Build all datasets from ``<dataset>.tsv`` files in ``tsv_dir``."""
        os.makedirs(out_dir, exist_ok=True)
        outputs = {}
        for dataset in DATASETS:
            tsv_path = os.path.join(tsv_dir, "%s.tsv" % dataset)
            outputs[dataset] = self.build_dataset(dataset, tsv_path, out_dir)
        return outputs


if __name__ == "__main__":
    import sys

    tsv_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "data/parquet"
    processor = NamesProcessor()
    built = processor.build_all(tsv_dir, out_dir)
    for name, path in built.items():
        print("Built %s -> %s" % (name, path))
