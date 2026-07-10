# -*- coding: UTF-8 -*-
import pytest

from russiannames.parser import NamesParser


@pytest.fixture(scope="module")
def parser():
    return NamesParser()


def test_parse_sfm_male(parser):
    assert parser.parse("Нигматуллин Ринат Ахметович") == {
        "format": "sfm",
        "sn": "Нигматуллин",
        "fn": "Ринат",
        "mn": "Ахметович",
        "gender": "m",
        "text": "Нигматуллин Ринат Ахметович",
        "parsed": True,
    }


def test_parse_surname_with_initials_female(parser):
    result = parser.parse("Петрова C.Я.")
    assert result["format"] == "sFM"
    assert result["sn"] == "Петрова"
    assert result["fn_s"] == "C"
    assert result["mn_s"] == "Я"
    assert result["gender"] == "f"
    assert result["parsed"] is True


@pytest.mark.parametrize(
    "text,fmt",
    [
        ("Исинбаев Иван Моисеевич", "sfm"),
        ("Иван Алексеевич", "fm"),
        ("Сидор Федоров", "fs"),
        ("Акимов Б.В.", "sFM"),
        ("А.Н. Хомяков", "FMs"),
    ],
)
def test_parse_formats(parser, text, fmt):
    result = parser.parse(text)
    assert result["parsed"] is True
    assert result["format"] == fmt


def test_parse_unrecognized(parser):
    result = parser.parse("Zzqxwv")
    assert result["parsed"] is False
    assert result["text"] == "Zzqxwv"


def test_gender_values_are_valid(parser):
    for text in ["Ольга Иванова", "Иван Петров", "Нигматуллин Ринат Ахметович"]:
        result = parser.parse(text)
        assert result["gender"] in {"m", "f", "u", "-"}


def test_no_arg_construction_and_data_dir_override(tmp_path):
    # Default construction must work without any server.
    NamesParser()
    # Overriding with a directory lacking datasets should fail lazily on lookup.
    p = NamesParser(data_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        p.parse("Иванов Иван Иванович")


def test_honorific_oglu_male_gender_preserved(parser):
    result = parser.parse("Алиев Гейдар Ага Оглы")
    assert result["format"] == "sfm"
    assert result["gender"] == "m"
    assert result["parsed"] is True


def test_honorific_kyzy_female_gender_preserved(parser):
    result = parser.parse("Алиева Лейла Ага Кызы")
    assert result["format"] == "sfm"
    assert result["gender"] == "f"
    assert result["parsed"] is True


def test_parse_single_first_name(parser):
    result = parser.parse("Ольга")
    assert result["parsed"] is True
    assert result["format"] == "f"
    assert result["fn"] == "Ольга"


def test_parse_single_surname(parser):
    result = parser.parse("Нигматуллин")
    assert result["parsed"] is True
    assert result["format"] == "s"
    assert result["sn"] == "Нигматуллин"


def test_import_from_package_root():
    import russiannames

    assert russiannames.NamesParser is NamesParser


def test_cli_main_runs(capsys):
    from russiannames.cli import main

    exit_code = main(["Нигматуллин Ринат Ахметович"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "sfm" in captured.out
