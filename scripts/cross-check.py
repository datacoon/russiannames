# -*- coding: UTF-8 -*-
import sys
import csv
from pprint import pprint

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

from russiannames.parser import NamesParser

FILENAME = '../data/raw/data-distinct.csv'
MAP_GENDER = {'f' : 0, 'm' : 1, 'u' : -1, '-' : -2}

    

def cross_check():
    np = NamesParser()
    f = open(FILENAME, 'r', encoding='utf8')
    reader = csv.DictReader(f, delimiter=',')
    print(','.join(['last_name', 'first_name', 'middle_name', 'gender_original', 'gender_identified']))
    for r in reader:
        c = np.classify(r['last_name'], r['first_name'], r['middle_name'])
        if 'gender' in c.keys():
            if c['gender'] == 'f' and r["sex"] == "0":
                continue
            if c['gender'] == 'm' and r["sex"] == "1":
                continue
            s = [r['last_name'], r['first_name'], r['middle_name'], r['sex'], str(MAP_GENDER[c['gender']])]
        else:
            s = [r['last_name'], r['first_name'], r['middle_name'], r['sex'], '-3']
        try:
            print(','.join(s))
        except:
            pass                               

if __name__ == '__main__':
    cross_check()