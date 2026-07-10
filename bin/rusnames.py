#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Thin wrapper kept for backwards compatibility; use the ``rusnames`` command."""

from russiannames.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
