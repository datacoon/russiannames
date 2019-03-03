====================================================
russiannames -- names parser, processing and gender identification for Russian names
====================================================

.. image:: https://img.shields.io/travis/datacoon/russiannames/master.svg?style=flat-square
    :target: https://travis-ci.org/datacoon/russiannames
    :alt: travis build status

.. image:: https://img.shields.io/pypi/v/russiannames.svg?style=flat-square
    :target: https://pypi.python.org/pypi/russiannames
    :alt: pypi version

.. image:: https://readthedocs.org/projects/russiannames/badge/?version=latest
    :target: http://russsiannames.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

`russiannames` is a Python 3 lib to parse Russian names, surnames and midnames, identify person gender by fullname and how name is written. It uses MongoDB as backend to speed-up name parsing



Documentation
=============

Documentation is built automatically and can be found on
`Read the Docs <https://russiannames.readthedocs.org/en/latest/>`_.


Features
========

Database of names used for identification
* 375449 surnames
* 32134 first names
* 48274 midnames

Supports 12 formats of Russian full names writing style

|format | example | description|
|---|---|---|
|f | Ольга | only first name|
|s | Петров | only surname|
|Fs | О. Сидорова | first letter of first name and full surname|
|sF | Николаев С. | full surname and first letter of surname|
|sf | Абрамов Семен | full surname and full first name|
|fs | Соня Камиуллина | full first name and full surname|
|fm | Иван Петрович | full first name and full middlename|
|SFM | М.Д.М. | first letters of surname, first name, middlename |
|FMs | А.Н. Егорова | first letters of first and middle name and full furname|
|sFM | Николаенко С.П. | full surname and first letters of first and middle names|
|sfM | Петракова Зинаида М.| full surname, first name and first letter of middle name|
|sfm | Казаков Ринат Артурович | full name as surname, first name and middle name|
|fms | Светлана Архиповна Волкова| full name as first name, middle name and surname|




Limitations
========

* very rare names, surnames or middlenames could be not parsed


Speed optimization
========

* preconfigured and preindexed MongoDb collections used


Usage
=====

The easiest way is to use the `russiannames.parser.NameParser <#russiannames.parser.NameParser>`_ class,
and it's `parse` function.

.. automodule:: russiannames.parser
   :members: NameParser


Examples
============


## Parse name and identify gender

    >>> from russiannames.parser import NamesParser
    >>> parser = NamesParser()
    >>> parser.parse('Нигматуллин Ринат Ахметович')
    {'format': 'sfm', 'sn': 'Нигматуллин', 'fn': 'Ринат', 'mn': 'Ахметович', 'gender': 'm', 'text': 'Нигматуллин Ринат Ахметович', 'parsed': True}
    >>> parser.parse('Петрова C.Я.')
    {'format': 'sFM', 'sn': 'Петрова', 'fn_s': 'C', 'mn_s': 'Я', 'gender': 'f', 'text': 'Петрова C.Я.', 'parsed': True}
    
## Ethnic identification (experimental)
    >>> from russiannames.parser import NamesParser
    >>> parser = NamesParser()
    >>> parser.classify('Нигматуллин', 'Ринат', 'Ахметович')
{'ethnics': ['tur'], 'gender': 'm'}
    >>> parser.classify('Алексеева', 'Ольга', 'Ивановна')
 {'ethnics': ['slav'], 'gender': 'f'}


Dependencies
============

`russiannames` relies on following libraries in some ways:

  * pymongo_ is a module for MongoDB.
.. _pymongo: https://pypi.python.org/pypi/pymongo


Supported languages
===================
* Russian



Requirements
============
* pymongo
* click https://github.com/pallets/click



Acknowledgements
================
