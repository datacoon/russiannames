# -*- coding: utf-8 -*-
"""Rule tables for gender and ethnicity heuristics.

These regex-based rules are used at runtime (:mod:`russiannames.parser`) and by
the dataset build pipeline (:mod:`russiannames.processor`) as a fallback when a
name is not present in the reference datasets.
"""

GENDER_MALE = 1
GENDER_FEMALE = 2
GENDER_BOTH = 0

# First-name suffix -> gender. Used by the dataset build pipeline.
NAME_POSTFIXES = {
    '^(.*)(и|ь|о|л)я$': GENDER_FEMALE,
    '^(.*)(н|л|г|р|с|т|з|д|м)а$': GENDER_FEMALE,
    '^(.*)(и|е)й$': GENDER_MALE,
    '^(.*)ав$': GENDER_MALE,
    '^(.*)и(р|с|д|н|м)$': GENDER_MALE,
    '^(.*)(а|я|о|е)н$': GENDER_MALE,
}

# Surname suffix -> gender.
SURNAME_POSTRULES = {
    '^(.*)(е|о|ё)в$': GENDER_MALE,
    '^(.*)(е|о|ё)ва$': GENDER_FEMALE,
    '^(.*)(и|ы)н$': GENDER_MALE,
    '^(.*)(и|ы)на$': GENDER_FEMALE,
    '^(.*)кий$': GENDER_MALE,
    '^(.*)(о|е)ва$': GENDER_FEMALE,
    '^(.*)(в|н)ич$': GENDER_BOTH,
    '^(.*)енко$': GENDER_BOTH,
    '^(.*)(л|н)юк$': GENDER_BOTH,
    '^(.*)(ы|и)х$': GENDER_BOTH,
    '^(.*)ый$': GENDER_MALE,
    '^(.*)ая$': GENDER_FEMALE,
    '^(.*)ун$': GENDER_BOTH,
    '^(.*)няк$': GENDER_BOTH,
    '^(.*)ец$': GENDER_BOTH,
    '^(.*)(р|ч|щ)ук$': GENDER_BOTH,
    '^(.*)ян$': GENDER_BOTH,
    '^(.*)дзе$': GENDER_BOTH,
    '^(.*)швили$': GENDER_BOTH,
    '^(.*)ой$': GENDER_MALE,
}

# Patronymic suffix -> gender.
MIDDLENAME_POSTRULES = {
    '^(.*)вич$': GENDER_MALE,
    '^(.*)вна$': GENDER_FEMALE,
}

# Ethnicity keys (see README for the full list of nine supported keys).
ETNOS_RUS = 'slav'
ETNOS_ARM = 'arm'
ETNOS_GEO = 'geor'
ETNOS_GREEK = 'greek'
ETNOS_GER = 'germ'
ETNOS_ARAB = 'arab'
ETNOS_JEW = 'jew'
ETNOS_POL = 'polsk'
ETNOS_TUR = 'tur'

# Surname suffix -> ethnicity key(s).
SURN_NATIONAL_RULES = {
    '^(.*)улла$': [ETNOS_ARAB],
    '^(.*)алла$': [ETNOS_ARAB],
    '^(.*)ян$': [ETNOS_ARM],
    '^(.*)янц$': [ETNOS_ARM],
    '^(.*)урт$': [ETNOS_GER],
    '^(.*)ерт$': [ETNOS_GER],
    '^(.*)орт$': [ETNOS_GER],
    '^(.*)бург$': [ETNOS_GER],
    '^(.*)ельд$': [ETNOS_GER],
    '^(.*)дт$': [ETNOS_GER],
    '^(.*)альд$': [ETNOS_GER],
    '^(.*)берг$': [ETNOS_GER],
    '^(.*)иди$': [ETNOS_GREEK],
    '^(.*)ади$': [ETNOS_GREEK],
    '^(.*)дзе$': [ETNOS_GEO],
    '^(.*)ия$': [ETNOS_GEO],
    '^(.*)ани$': [ETNOS_GEO],
    '^(.*)швили$': [ETNOS_GEO],
}
