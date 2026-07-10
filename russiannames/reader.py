# -*- coding: UTF-8 -*-
"""Aggregate raw ``surname firstname patronymic`` records into frequency tables.

This is a pre-dataset stage: it walks a directory tree of raw text files (one
``surname firstname midname`` triple per line) and produces frequency-sorted TSV
files for names, surnames and midnames. Python 3, UTF-8 text I/O only.
"""

import os
import sys


class NameReader:
    def __init__(self, path, out_dir="."):
        self.path = path
        self.out_dir = out_dir
        self.names = {}
        self.surnames = {}
        self.midnames = {}
        self.n = 0

    def process(self):
        all_path = os.path.join(self.out_dir, "all.txt")
        other_path = os.path.join(self.out_dir, "not3.txt")
        with open(all_path, "w", encoding="utf-8") as f_all, \
                open(other_path, "w", encoding="utf-8") as f_other:
            for entry in os.listdir(self.path):
                self.process_dir(os.path.join(self.path, entry), f_all, f_other)

    def process_dir(self, dirname, f_all, f_other):
        if not os.path.isdir(dirname):
            return
        for fname in os.listdir(dirname):
            filename = os.path.join(dirname, fname)
            with open(filename, encoding="utf-8") as f:
                lines = f.read().splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) != 3:
                    f_other.write(line + "\n")
                    self.n += 1
                    continue
                surname, name, midname = parts
                self.names[name] = self.names.get(name, 0) + 1
                self.surnames[surname] = self.surnames.get(surname, 0) + 1
                self.midnames[midname] = self.midnames.get(midname, 0) + 1
                f_all.write(line + "\n")

    def write_dict(self, data, filename):
        path = os.path.join(self.out_dir, filename)
        ordered = sorted(data.items(), key=lambda kv: kv[1], reverse=True)
        with open(path, "w", encoding="utf-8") as f:
            for key, value in ordered:
                f.write("%s\t%d\n" % (key, value))

    def save(self):
        self.write_dict(self.names, "names.tsv")
        self.write_dict(self.surnames, "surnames.tsv")
        self.write_dict(self.midnames, "midnames.tsv")


def name_parse(dirname, out_dir="."):
    reader = NameReader(dirname, out_dir=out_dir)
    reader.process()
    reader.save()
    print(reader.n)
    print(len(reader.names), len(reader.midnames), len(reader.surnames))
    top = sorted(reader.names.items(), key=lambda kv: kv[1], reverse=True)
    for key, value in top[:50]:
        print(value, key)


if __name__ == "__main__":
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    name_parse(sys.argv[1], out_dir=out)
