# -*- coding: utf-8 -*-
GENDER_MALE = 1
GENDER_FEMALE = 2
GENDER_BOTH = 0

NAME_POSTFIXES = {
                  u'^(.*)(и|ь|о|л)я$' : GENDER_FEMALE,
                  u'^(.*)(н|л|г|р|с|т|з|д|м)а$' : GENDER_FEMALE,
                  u'^(.*)(и|е)й$' : GENDER_MALE,
                  u'^(.*)ав$' : GENDER_MALE,
                  u'^(.*)и(р|с|д|н|м)$' : GENDER_MALE,
                  u'^(.*)(а|я|о|е)н$' : GENDER_MALE,
}

NAME_POSTRULES = {
                  u'^(.*)ий$' : {'male' : u'-ий +ьевич', 'female': u'-ий +евна'},
                  u'^(.*)ей$' : {'male' : u'-й +евич', 'female': u'-й +евна'},
                  u'^(.*)(р|л)ь$' : {'male' : u'-ь +евич', 'female': u'-ь +евна'},
                  u'^(.*)и(и|р|с|д|н|м)$' : {'male' : u'+ович', 'female': u'+овна'},
                  u'^(.*)(а|я|о|е)н$' : {'male' : u'+ович', 'female': u'+овна'},
                  u'^(.*)(а|о|е)м$' : {'male' : u'+ович', 'female': u'+овна'},
}

SURNAME_POSTRULES = {
                     u'^(.*)(е|о|ё)в$' : GENDER_MALE,
                     u'^(.*)(е|о|ё)ва$' : GENDER_FEMALE,
                     u'^(.*)(и|ы)н$' : GENDER_MALE,
                     u'^(.*)(и|ы)на$' : GENDER_FEMALE,
                     u'^(.*)кий$' : GENDER_MALE,
                     u'^(.*)(о|е)ва$' : GENDER_FEMALE,
                     u'^(.*)(в|н)ич$' : GENDER_BOTH,
                     u'^(.*)енко$' : GENDER_BOTH,
                     u'^(.*)(л|н)юк$' : GENDER_BOTH,
                     u'^(.*)(ы|и)х$' : GENDER_BOTH,
                     u'^(.*)ый$' : GENDER_MALE,
                     u'^(.*)ая$' : GENDER_FEMALE,
                     u'^(.*)ун$' : GENDER_BOTH,
                     u'^(.*)няк$' : GENDER_BOTH,
                     u'^(.*)ец$' : GENDER_BOTH,
                     u'^(.*)(р|ч|щ)ук$' : GENDER_BOTH,
                     u'^(.*)ян$' : GENDER_BOTH,
                     u'^(.*)дзе$' : GENDER_BOTH,
                     u'^(.*)швили$' : GENDER_BOTH,
                     u'^(.*)ой$' : GENDER_MALE,
}

MIDDLENAME_POSTRULES = {
                     u'^(.*)вич$' : GENDER_MALE,
                     u'^(.*)вна$' : GENDER_FEMALE,
}

ETNOS_RUS = u'slav'
ETNOS_ARM = u'arm'
ETNOS_GEO = u'geor'
ETNOS_GREEK = u'greek'
ETNOS_GER = u'germ'
ETNOS_ARAB = u'arab'


SURN_NATIONAL_RULES = {
    u'^(.*)улла$' : [ETNOS_ARAB, ],
    u'^(.*)алла$' : [ETNOS_ARAB, ],
    u'^(.*)ян$' : [ETNOS_ARM, ],
    u'^(.*)янц$' : [ETNOS_ARM, ],
    u'^(.*)урт$' : [ETNOS_GER, ],
    u'^(.*)ерт$' : [ETNOS_GER, ],
    u'^(.*)орт$' : [ETNOS_GER, ],
    u'^(.*)бург$' : [ETNOS_GER, ],
    u'^(.*)ельд$' : [ETNOS_GER, ],
    u'^(.*)дт$' : [ETNOS_GER, ],
    u'^(.*)альд$' : [ETNOS_GER, ],
    u'^(.*)берг$' : [ETNOS_GER, ],
    u'^(.*)иди$' : [ETNOS_GREEK, ],
    u'^(.*)ади$' : [ETNOS_GREEK, ],
    u'^(.*)дзе$' : [ETNOS_GEO, ],
    u'^(.*)ия$' : [ETNOS_GEO, ],
    u'^(.*)ани$' : [ETNOS_GEO, ],
    u'^(.*)швили$' : [ETNOS_GEO,],

}

MIDDLENAME_POSTRULES = {
                     '^(.*)вич$' : GENDER_MALE,
                     '^(.*)вна$' : GENDER_FEMALE,
}

