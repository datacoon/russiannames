# -*- coding: UTF-8 -*-

import logging
import re
from typing import Optional

from .consts import (
    GENDER_FEMALE,
    GENDER_MALE,
    MIDDLENAME_POSTRULES,
    SURN_NATIONAL_RULES,
    SURNAME_POSTRULES,
)
from .datastore import NamesDatastore


def use_rule(name: str, rule: str) -> str:
    """Use one of rules and apply it to identification"""
    result = name
    parts = rule.split()
    for part in parts:
        if part[0] == '-':
            shift = len(part[1:])
            result = result[:-shift]
        elif part[0] == '+':
            result = result + part[1:]
    return result


def guess_by_rules(name: str, rules: dict) -> Optional[tuple]:
    """matches against rules"""
    for key, value in list(rules.items()):
        if re.match(key, name):
            return (key, value)
    return None


def norm_name(text: str) -> str:
    return text.strip('.').title()


class NamesParser:
    def __init__(self, data_dir: Optional[str] = None) -> None:
        self._store = NamesDatastore(data_dir=data_dir)

    def parse(self, text: str) -> dict:
        result = {}
        store = self._store
        p = re.compile(r'\.|\s')
        parts = p.split(text)
        parts2 = list(map(norm_name, parts))
        parts = [part for part in parts2 if len(part) != 0]
        if len(parts) == 1:
            the_n = store.find_one('names', parts[0])
            if the_n:
                result  = {'format' : 'f','fn' : parts[0]}
            else:
                the_s = store.find_one('surnames', parts[0])
                if the_s:
                    result  = {'format' : 's','sn' : parts[0]}
        elif len(parts) == 2:
            if len(parts[0]) == 1 and len(parts[1]) > 1:
                result = {'format' : 'Fs', 'sn' : parts[1], 'fn_s' : parts[0]}
            elif len(parts[1]) == 1 and len(parts[0]) > 1:
                result = {'format' : 'sF', 'sn' : parts[0], 'fn_s' : parts[1]}
            else:
                the_n1 = store.find_one('names', parts[0])
                the_n2 = store.find_one('names', parts[1])
                if not the_n1 and the_n2:
                    result  = {'format' : 'sf', 'sn' : parts[0], 'fn' : parts[1]}
                elif the_n1 and the_n2:
                    if the_n2['count'] > the_n1['count']:
                        result  = {'format' : 'sf', 'sn' : parts[0], 'fn' : parts[1]}
                    else:
                        the_m = store.find_one('midnames', parts[1])
                        if the_m:
                            result  = {'format' : 'fm', 'mn' : parts[1], 'fn' : parts[0]}
                        else:
                            result  = {'format' : 'fs', 'sn' : parts[1], 'fn' : parts[0]}
                elif the_n1 and not the_n2:
                    the_m = store.find_one('midnames', parts[1])
                    if the_m:
                        result  = {'format' : 'fm', 'mn' : parts[1], 'fn' : parts[0]}
                    else:
                        result  = {'format' : 'fs', 'sn' : parts[1], 'fn' : parts[0]}
                else:
                    res = guess_by_rules(parts[0], SURNAME_POSTRULES)
                    if res:
                        result = {'format': 'sf', 'sn' : parts[0], 'fn' : parts[1]}
                        if res[1] == GENDER_MALE:
                            result['gender'] = 'm'
                        elif res[1] == GENDER_FEMALE:
                            result['gender'] = 'f'
        elif len(parts) == 3:
            if len(parts[0]) == 1:
                if len(parts[1]) == 1:
                    if len(parts[2]) == 1:
                        result = {'format': 'SFM', 'sn_s': parts[0],
                                  'fn_s': parts[1], 'mn_s': parts[2]}
                    else:
                        result = {'format': 'FMs', 'sn': parts[2],
                                  'fn_s': parts[0], 'mn_s': parts[1]}

            elif len(parts[1]) == 1:
                if len(parts[2]) == 1:
                    result = {'format': 'sFM', 'sn': parts[0],
                              'fn_s': parts[1], 'mn_s': parts[2]}
            else:
                if len(parts[2]) == 1:
                    result = {'format': 'sfM', 'sn': parts[0],
                              'fn': parts[1], 'mn_s': parts[2]}
                else:
                    the_m = store.find_one('midnames', parts[2])
                    if the_m:
                        result = {'format': 'sfm', 'sn': parts[0],
                                  'fn': parts[1], 'mn': parts[2]}
                    else:
                        res = guess_by_rules(parts[2], MIDDLENAME_POSTRULES)
                        if res:
                            result = {'format': 'sfm', 'sn': parts[0],
                                      'fn': parts[1], 'mn': parts[2]}
                            if res[1] == GENDER_MALE:
                                result['gender'] = 'm'
                            elif res[1] == GENDER_FEMALE:
                                result['gender'] = 'f'
                        else:
                            the_n = store.find_one('names', parts[0])
                            if the_n:
                                result = {'format': 'fms', 'sn': parts[2],
                                          'fn': parts[0], 'mn': parts[1]}
                            else:
                                the_n = store.find_one('names', parts[1])
                                if the_n:
                                    result = {'format': 'sfm', 'sn': parts[0],
                                              'fn': parts[1], 'mn': parts[2]}
        elif len(parts) == 4:
            if parts[3] == 'Оглы':
                result = {'format': 'sfm', 'sn': parts[0], 'fn': parts[1],
                          'mn': ' '.join(parts[2:3]), 'gender': 'm'}
            elif parts[3] == 'Кызы':
                result = {'format': 'sfm', 'sn': parts[0], 'fn': parts[1],
                          'mn': ' '.join(parts[2:3]), 'gender': 'f'}


        if not result or 'format' not in result:
            result['parsed'] = False
            result['text'] = text
            return result

        # Only (re-)derive gender when a parse branch has not already established
        # a definitive value. Genders set by the honorific (Оглы/Кызы), rule, or
        # dataset branches above are authoritative and must be preserved.
        if result.get('gender') not in ('m', 'f'):
            result['gender'] = '-'
            if 'mn' in result:
                m = store.find_one('midnames', result['mn'])
                if m and 'gender' in m:
                    result['gender'] = m['gender']
                else:
                    res = guess_by_rules(result['mn'], MIDDLENAME_POSTRULES)
                    if res:
                        if res[1] == GENDER_MALE:
                            result['gender'] = 'm'
                        elif res[1] == GENDER_FEMALE:
                            result['gender'] = 'f'
            if 'fn' in result:
                n = store.find_one('names', result['fn'])
                if n and 'gender' in n:
                    result['gender'] = n['gender']
            if 'sn' in result and result['gender'] in ['u', '-']:
                s = store.find_one('surnames', result['sn'])
                if s and 'gender' in s:
                    result['gender'] = s['gender']
                else:
                    res = guess_by_rules(result['sn'], SURNAME_POSTRULES)
                    if res:
                        if res[1] == GENDER_MALE:
                            result['gender'] = 'm'
                        elif res[1] == GENDER_FEMALE:
                            result['gender'] = 'f'
        result['text'] = text
        result['parsed'] = True
        return result

    def classify(self, sn: str, fn: str, mn: str) -> dict:
        result = {}
        store = self._store
        genders = {}
        ethnics = []
        the_m = store.find_one('midnames', mn)
        logging.debug('Last name %s, first name %s, middle name %s' % (sn, fn, mn))
        if the_m:
            logging.debug('Middle name found in db %s' % (str(the_m)))
            if 'gender' in the_m:
                v = genders.get(the_m['gender'], 0)
                genders[the_m['gender']] = v + 1
            if 'ethnic' in the_m:
                for e in the_m['ethnic']:
                    if e not in ethnics:
                        ethnics.append(e)
        else:
            res = guess_by_rules(mn, MIDDLENAME_POSTRULES)
            logging.debug('Rules result on middle name %s' % (str(res)))
            if res:
                if res[1] == GENDER_MALE:
                    g = 'm'
                elif res[1] == GENDER_FEMALE:
                    g = 'f'
                else:
                    g = 'u'
                v = genders.get(g, 0)
                genders[g] = v + 1
        the_m = store.find_one('names', fn)
        if the_m:
            if 'gender' in the_m:
                v = genders.get(the_m['gender'], 0)
                genders[the_m['gender']] =  v + 1
            if 'ethnic' in the_m:
                for e in the_m['ethnic']:
                    if e not in ethnics:
                        ethnics.append(e)

        the_m = store.find_one('surnames', sn)
        if the_m:
            if 'gender' in the_m:
                v = genders.get(the_m['gender'], 0)
                genders[the_m['gender']] = v + 1
            if 'ethnic' in the_m:
                for e in the_m['ethnic']:
                    if e not in ethnics:
                        ethnics.append(e)
        else:
            res = guess_by_rules(sn, SURNAME_POSTRULES)
            if res:
                if res[1] == GENDER_MALE:
                    g = 'm'
                elif res[1] == GENDER_FEMALE:
                    g = 'f'
                else:
                    g = 'u'
                v = genders.get(g, 0)
                genders[g] = v + 1
        res = guess_by_rules(sn, SURN_NATIONAL_RULES)
        if res:
            for r in res[1]:
                if r not in ethnics:
                    ethnics.append(r)
        alist = list(genders.items())
        logging.debug('Genders list %s' % (genders))
        thedict = sorted(alist, key=lambda x: x[1], reverse=True)
        result['ethnics'] = ethnics
        if len(thedict) > 1 and thedict[0][0] == 'u':
            result['gender'] = thedict[1][0]
        elif len(thedict) > 0:
            result['gender'] = thedict[0][0]
        return result



if __name__ == '__main__':
    np = NamesParser()
    print(np.parse('Исинбаев Иван Моисеевич'))
    print(np.parse('Иванов Шалва Ицхакович'))
    print(np.parse('Иван Алексеевич'))
    print(np.parse('Сидор Федоров'))
    print(np.parse('Акимов Б.В.'))
    print(np.parse('А.Н. Хомяков'))
    print(np.classify('Козлевич', 'Иннокентий', 'Мафусаилович'))
