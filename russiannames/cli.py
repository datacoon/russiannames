# -*- coding: UTF-8 -*-
"""Command-line interface for russiannames."""

import argparse
from pprint import pprint

from . import __version__
from .parser import NamesParser


def build_arg_parser():
    ap = argparse.ArgumentParser(
        prog="rusnames",
        description="Parse a Russian full name and identify its format and gender.",
    )
    ap.add_argument("name", help="Full name string to parse, e.g. 'Иванов Иван Иванович'")
    ap.add_argument(
        "--data-dir",
        default=None,
        help="Directory with names/surnames/midnames Parquet datasets "
        "(defaults to the bundled datasets or $RUSSIANNAMES_DATA_DIR).",
    )
    ap.add_argument("--version", action="version", version="%%(prog)s %s" % __version__)
    return ap


def main(argv=None):
    args = build_arg_parser().parse_args(argv)
    parser = NamesParser(data_dir=args.data_dir)
    pprint(parser.parse(args.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
