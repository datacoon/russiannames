# -*- coding: UTF-8 -*-
"""Cross-check gender classification accuracy against a labelled benchmark.

Reads the labelled dataset directly from the committed zip archive
(``data/raw/data-distinct.zip``) so the benchmark runs on a fresh checkout with
no manual extraction step. Prints per-row mismatches followed by an accuracy
summary.
"""

import csv
import io
import logging
import os
import zipfile

from russiannames.parser import NamesParser

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

ZIP_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "raw", "data-distinct.zip"
)
CSV_MEMBER = "data-distinct.csv"
MAP_GENDER = {"f": 0, "m": 1, "u": -1, "-": -2}
# Benchmark encodes sex as "0" (female) and "1" (male).
SEX_TO_GENDER = {"0": "f", "1": "m"}


def _open_rows(zip_path=ZIP_PATH, member=CSV_MEMBER):
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(member) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8")
            yield from csv.DictReader(text, delimiter=",")


def cross_check(zip_path=ZIP_PATH):
    np = NamesParser()
    total = 0
    evaluated = 0
    correct = 0
    print(",".join(
        ["last_name", "first_name", "middle_name", "gender_original", "gender_identified"]
    ))
    for r in _open_rows(zip_path):
        if not (r.get("last_name") or r.get("first_name") or r.get("middle_name")):
            continue
        total += 1
        c = np.classify(r["last_name"], r["first_name"], r["middle_name"])
        identified = c.get("gender")
        expected = SEX_TO_GENDER.get(r.get("sex"))
        if identified in ("m", "f") and expected is not None:
            evaluated += 1
            if identified == expected:
                correct += 1
                continue
            code = MAP_GENDER[identified]
        else:
            code = -3
        print(",".join([
            r["last_name"], r["first_name"], r["middle_name"], r.get("sex", ""), str(code),
        ]))

    accuracy = (correct / evaluated) if evaluated else 0.0
    logging.info(
        "rows=%d evaluated=%d correct=%d accuracy=%.4f",
        total, evaluated, correct, accuracy,
    )
    return accuracy


if __name__ == "__main__":
    cross_check()
