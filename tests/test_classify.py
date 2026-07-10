# -*- coding: UTF-8 -*-
import pytest

from russiannames.parser import NamesParser


@pytest.fixture(scope="module")
def parser():
    return NamesParser()


def test_classify_turkic_male(parser):
    assert parser.classify("Нигматуллин", "Ринат", "Ахметович") == {
        "ethnics": ["tur"],
        "gender": "m",
    }


def test_classify_slavic_female(parser):
    assert parser.classify("Алексеева", "Ольга", "Ивановна") == {
        "ethnics": ["slav"],
        "gender": "f",
    }


def test_classify_ethnics_deduplicated(parser):
    result = parser.classify("Иванов", "Иван", "Иванович")
    assert result["ethnics"] == list(dict.fromkeys(result["ethnics"]))
