# Russian Names


`russiannames` is a Python 3 library dedicated to parse Russian names, surnames and midnames, identify person gender by fullname and how name is written. It uses MongoDB as backend to speed-up name parsing.



## Documentation

Documentation is built automatically and can be found on
https://russiannames.readthedocs.org/en/latest/

## Installation

To install Python library use `pip install russiannames` via pip or `python setup.py install` 

To use database you need MongoDB instance. 
Unpack db_data_bson.zip file from https://github.com/datacoon/russiannames/blob/master/data/bson/db_dump_bson.zip

and use `mongorestore` command to restore `names` database with 3 collections: names, surnames and midnames

## Features

Database of names used for identification

* 375449 surnames - collection: surnames
* 32134 first names - collection: names
* 48274 midnames - collection: midnames

Detailed database statistics by gender and collection

| collection| total | males|females|universal or unidentified |
| --- | --- | --- | --- | --- |
| names | 32134 | 19297 | 8278 | 1196 |
| midnames | 48274 | 30114 | 16143 | 0 |
| surnames | 375274 | 124662 | 111534 | 38827 |


Supports 12 formats of Russian full names writing style

| Format | Example        | Description  |
| ------ | -------------- | ------------ |
| f | Ольга | only first name |
| s | Петров | only surname |
| Fs | О. Сидорова | first letter of first name and full surname |
| sF | Николаев С. | full surname and first letter of surname |
| sf | Абрамов Семен | full surname and full first name |
| fs | Соня Камиуллина | full first name and full surname |
| fm | Иван Петрович | full first name and full middlename |
| SFM | М.Д.М. | first letters of surname, first name, middlename |
| FMs | А.Н. Егорова | first letters of first and middle name and full furname |
| sFM | Николаенко С.П. | full surname and first letters of first and middle names |
| sfM | Петракова Зинаида М. | full surname, first name and first letter of middle name |
| sfm | Казаков Ринат Артурович | full name as surname, first name and middle name |
| fms | Светлана Архиповна Волкова | full name as first name, middle name and surname |


Supports names with following ethnics identification

9 ethnic types in names, surnames and middle names supported

| key  | name (en) | name (rus)
| ---- | --------- | ----------
| arab | Arabic     | Арабское
| arm  | Armenian     | Армянское
| geor | Georgian     | Грузинское
| germ | German     | Немецкие
| greek | Greek    | Греческие
| jew  | Jew      | Еврейские
| polsk | Polish    | Польские
| slav | Slavic (Russian) | Славянские
| tur  | Turkic | Тюркские (тюркоязычные)


## Limitations

* very rare names, surnames or middlenames could be not parsed 
* ethnic identification is still on early stage


## Speed optimization

* preconfigured and preindexed MongoDb collections used


## Usage and Examples

### Parse name and identify gender

Parses names and returns: format, surname, first name, middle name, parsed (True/False) and gender 

    >>> from russiannames.parser import NamesParser
    >>> parser = NamesParser()
    >>> parser.parse('Нигматуллин Ринат Ахметович')
    {'format': 'sfm', 'sn': 'Нигматуллин', 'fn': 'Ринат', 'mn': 'Ахметович', 'gender': 'm', 'text': 'Нигматуллин Ринат Ахметович', 'parsed': True}
    >>> parser.parse('Петрова C.Я.')
    {'format': 'sFM', 'sn': 'Петрова', 'fn_s': 'C', 'mn_s': 'Я', 'gender': 'f', 'text': 'Петрова C.Я.', 'parsed': True}

Gender field could have one of following values:

* m: Male
* f: Female
* u: Unknown / unidentified
* -: Impossible to identify
    
### Ethnic identification (experimental)
Parses surname, first name and middle name and tries to identify person ethic affiliation of the person

    >>> from russiannames.parser import NamesParser
    >>> parser = NamesParser()
    >>> parser.classify('Нигматуллин', 'Ринат', 'Ахметович')
    {'ethnics': ['tur'], 'gender': 'm'}
    >>> parser.classify('Алексеева', 'Ольга', 'Ивановна')
    {'ethnics': ['slav'], 'gender': 'f'}


## Supported languages
* Russian


## Requirements
* pymongo
* click

## Related projects
- Slavic names https://github.com/wb-08/SlavicNames - same data shipped as SQLite database
