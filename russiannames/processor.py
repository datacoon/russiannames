# -*- coding: UTF-8 -*-

import sys, os.path
from pymongo import MongoClient
import re
from .consts import *

def use_rule(name, rule):
    """"""
    result = name
    parts = rule.split()
    for part in parts:
        if part[0] == '-':
            shift = len(part[1:])
            result = result[:-shift]
        elif part[0] == '+':
            result = result + part[1:]
    return result



def guess_by_rules(name, rules):
    """matches against rules"""
    for key, value in list(rules.items()):
        if re.match(key, name):
            return (key, value)
    return None

def guess_gender_by_name(name):
    """Предполагает пол по имени"""
    for key, value in list(NAME_POSTFIXES.items()):
        if re.match(key, name):
            return (key, value)
    return None

def guess_gender_by_surname(name):
    """Предполагает пол по имени"""
    for key, value in list(SURNAME_POSTRULES.items()):
        if re.match(key, name):
            return (key, value)
    return None



def guess_name_to_middlename(name):
    """Предполагает правило формирования отчества по имени"""
    for key, value in list(NAME_POSTRULES.items()):
        if re.match(key, name):
            return value
    return None


def norm_name(text):
    return text.strip('.').title()



NAMES_DB = 'names'

class NamesProcessor:
    def __init__(self):
        self._conn = MongoClient()
        self._db = self._conn[NAMES_DB]
        pass

    def _gettype(self, v, t):
        if t == 'int':
            return int(v)
        elif t == 'string':
            return v
        elif t == 'float':
            return float(v)

    def load_data(self, cname, filename, schema={}):
        print(('Loading %s into %s' %(filename, cname)))
        coll = self._db[cname]
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().decode('utf8').split('\t')
                i = 0
                item = {}
                for p in parts:
                    i += 1
                    sc = schema[str(i)]
                    item[sc['name']] = self._gettype(p, sc['type'])
                    coll.save(item)

    def load_names(self):
        self.load_data(cname='surnames', filename='surnames.tsv', schema={'1' : {'name' : 'text', 'type' : 'string'}, '2' : {'name' : 'count', 'type' : 'int'}})
        self.load_data(cname='midnames', filename='midnames.tsv', schema={'1' : {'name' : 'text', 'type' : 'string'}, '2' : {'name' : 'count', 'type' : 'int'}})
        self.load_data(cname='names', filename='names.tsv', schema={'1' : {'name' : 'text', 'type' : 'string'}, '2' : {'name' : 'count', 'type' : 'int'}})
        self.load_data(cname='fullnames', filename='all.txt', schema={'1' : {'name' : 'text', 'type' : 'string'}})

    def import_new_names(self, filename):
        f = open(filename)
        lines = f.read().splitlines()
        f.close()
        i = 0
        fcoll = self._db['fullnames']
        ncoll = self._db['names']
        mcoll = self._db['midnames']
        scoll = self._db['surnames']
        for line in lines:
            line = line.decode('utf8').strip()
            if i % 1000 == 0: print(i)
            i += 1
            if i < 5007000: continue
            parts = line.split('\t')
            if len(parts) != 3:
                continue
            else:
                (surname, fname, mname) = parts
                if len(fname) == 1 or len(mname) == 1: continue
                if (len(fname) == 2 and fname[1] == '.') or (len(mname) == 2 and mname[1] == '.'): continue
                # Saving fullnames
                o = fcoll.find_one({'name.fn' : fname, 'name.sn' : surname, 'name.mn' : mname})
                if not o:
                    o = {'text' : ' '.join([surname, fname, mname]), 'parsed' : 1, 'name': {'fn' : fname, 'sn' : surname, 'mn' : mname}}
                    fcoll.save(o)
                else:
                    continue
                # Saving surname
                o = scoll.find_one({'text' : surname})
                if not o:
                    o = {'text' : surname, 'count' : 1}
                else:
                    o['count'] += 1
                scoll.save(o)
                # Saving name
                o = ncoll.find_one({'text' : fname})
                if not o:
                    o = {'text' : fname, 'count' : 1}
                else:
                    o['count'] += 1
                ncoll.save(o)
                # Saving midname
                o = mcoll.find_one({'text' : mname})
                if not o:
                    o = {'text' : mname, 'count' : 1}
                else:
                    o['count'] += 1
                mcoll.save(o)


    def fullnames_parse(self):
        """Разбор ФИО в фамилию, имя и отчество"""
        print('Parsing fullnames')
        i = 0
        coll = self._db['fullnames']
        for o in coll.find():
            i += 1
            if i % 1000 == 0:
                print(('Processed %d' %(i)))
            if 'parsed' in o and o['parsed'] != 1:
                continue
            parts = o['text'].split()
            if len(parts) != 3:
                o['parsed'] = 0
            else:
                o['name'] = {'sn' : parts[0], 'fn' : parts[1], 'mn' : parts[2]}
                o['parsed'] = 1
            coll.save(o)

    def midnames_gender_recognize(self):
        """Распознавание пола по отчеству"""
        coll = self._db['midnames']
        i = 0
        total = {'m' : 0, 'f' : 0, 'u' : 0}
        for o in coll.find():
            i += 1
            if i % 1000 == 0:
                print(('Processed %d' %(i), total))
            name = o['text']
            if len(name) > 3:
                if name[-2:] == 'ич':
                    o['gender'] = 'm'
                elif name[-3:] in ['вна', 'чна', 'шна']:
                    o['gender'] = 'f'
                elif name[-4:] == 'оглы':
                    o['gender'] = 'm'
                elif name[-4:] == 'Оглы':
                    o['gender'] = 'm'
                elif name[-4:] == 'Кызы':
                    o['gender'] = 'f'
                else:
                    o['gender'] = 'u'
            else:
                o['gender'] = 'u'
            v = total.get(o['gender'], 0)
            total[o['gender']] += 1
            if 'gender' in o:
                coll.save(o)
        print(total)
        pass

    def surnames_gender_recognize(self):
        """Распознавание пола фамилий"""
        coll = self._db['surnames']
        coll.create_index('count', -1)
        ncoll = self._db['names']
        for o in coll.find().sort('count', -1):
            name = o['text']
            res = guess_gender_by_surname(name)
            if not res:
#                print o['text'].encode('cp866'), o['count']
                continue
            else:
                print((o['text']))
                if res[1] == GENDER_MALE:
                    o['gender'] = 'm'
                elif res[1] == GENDER_FEMALE:
                    o['gender'] = 'f'
                elif res[1] == GENDER_BOTH:
                    o['gender'] = 'u'
                coll.save(o)


    def map_names_midnames(self):
        """Соотнесение имени и отчества"""
        coll = self._db['midnames']
#        coll.create_index('fname', -1)
#        coll.create_index('count', -1)
        ncoll = self._db['names']
        i = 0
        z = 0
        for o in coll.find({'fname' : {'$exists' : False}}).sort('count', -1):
            i += 1
            if i % 1000 == 0:
                print(('Processed %d of %d ' %(z, i)))
            name = o['text']
            short = None
            if len(name) > 3:
                if name[-4:] == 'ович':
                    short = name[:-4]
                elif name[-4:] == 'овна':
                    short = name[:-4]
                elif name[-4:] == 'ична':
                    short = name[:-4] + 'а'
                elif name[-6:] == 'инична':
                    short = name[:-4] + 'а'
                elif name[-5:] == 'ьевич':
                    short = name[:-5] + 'ий'
                elif name[-5:] == 'иевич':
                    short = name[:-5] + 'ий'
                elif name[-5:] == 'левич':
                    short = name[:-5] + 'ль'
                elif name[-5:] == 'ревич':
                    short = name[:-5] + 'рь'
                elif name[-5:] == 'ьевич':
                    short = name[:-5] + 'ь'
                elif name[-5:] == 'еевич':
                    short = name[:-5] + 'ей'
                elif name[-5:] == 'ьевна':
                    short = name[:-5] + 'ий'
                elif name[-5:] == 'иевна':
                    short = name[:-5] + 'ий'
                elif name[-5:] == 'ревна':
                    short = name[:-5] + 'рь'
                elif name[-5:] == 'левна':
                    short = name[:-5] + 'ль'
                elif name[-5:] == 'еевич':
                    short = name[:-5] + 'ей'
                elif name[-5:] == 'еевна':
                    short = name[:-5] + 'ей'
                elif name[-5:] == 'аевич':
                    short = name[:-5] + 'ай'
                elif name[-5:] == 'аевна':
                    short = name[:-5] + 'ай'
#                else:
#                    print name.encode('utf8'), o['count']
#                    continue
            else:
                continue
            if short:
#                print short.encode('cp866')
                n = ncoll.find_one({'text' : short})
                if n:
                    o['fname'] = short
                    coll.save(o)
                    z += 1
                    n['gender'] = 'm'
                    ncoll.save(n)



    def fullnames_map_gender(self, dataskip=0, datalimit=50000):
        """Recognize fullnames gender"""
        coll = self._db['fullnames']
        coll.create_index('count', -1)
        coll.create_index('parsed', -1)
        mcoll = self._db['midnames']
        all = []
        print(('Populating data', dataskip, datalimit))
        i = 0
        thed = coll.find({'gender' : {'$exists' : False}}).skip(dataskip).limit(datalimit)

        for o in thed:
            i += 1
            if i % 1000 == 0:
                print(('Populating %d' %(i)))
            all.append(o)
        print('Processing data')
        i = 0
        n = 0
        for o in all:

            i += 1
            if i % 10000 == 0:
                print(('Populating %d of %d (%f)' %(n, i, (n*100.0) / i)))
            m = mcoll.find_one({'text' : o['name']['mn']})
            if m:
                o['gender'] = m['gender']
                coll.save(o)
                n += 1

    def map_names_fullnames(self):
        ncoll = self._db['names']
        mcoll = self._db['midnames']
        fcoll = self._db['fullnames']
        for o in ncoll.find({'gender' : {'$exists' : False}}):
#            if not str(o['gender']).isdigit():
#                continue
            gender = {}
            for n in fcoll.find({'name.fn' : o['text']}):
                if 'gender' in n:
                    v = gender.get(n['gender'], 0)
                    gender[n['gender']] = v + 1
                else:
                    mname = n['name']['mn']
                    m = mcoll.find_one({'text' : mname})
                    if m and 'gender' in m:
                        v = gender.get(m['gender'], 0)
                        gender[m['gender']] = v + 1
            if len(list(gender.keys())) == 1:
                o['gender'] = list(gender.keys())[0]
                ncoll.save(o)
            elif len(list(gender.keys())) == 2:
                keys = list(gender.keys())
                if gender[keys[0]] > gender[keys[1]]:
                    o['gender'] = keys[0]
                else:
                    o['gender'] = keys[1]
                ncoll.save(o)
            elif len(list(gender.keys())) > 2:
                m = None
                for k, v in list(gender.items()):
                    if not m:
                        m = [k, v]
                    else:
                        if m[1] < v:
                            m = [k, v]
                o['gender'] = m[0]
                ncoll.save(o)
            print((o['text'], o['gender'] if 'gender' in o else '', gender))

    def verify_names(self, filename):
        f = open(filename, 'r')
        ncoll = self._db['midnames']
        i = 0
        names = {}
        for l in f:
            i +=  1
            parts = l.decode('utf8').split()
            if i % 1000 == 0:
                print(i)
            if len(parts) == 3:
                name = parts[2].title()
                item = ncoll.find_one({'text' : name})
                if item:
                    v = names.get(name, 0)
                    names[name] = v + 1

        thedict = sorted(list(names.items()), key=lambda x, y: x[1], reverse=True)
        print((len(thedict)))
        for n, v in thedict[0:20]:
            print((n, v))


    def map_national_surnames(self):
        ncoll = self._db['surnames']
        print((ncoll.count()))
        n = 0
        i = 0
        for o in ncoll.find():
            i += 1
            if i % 1000 == 0:
                print(i)
            result = guess_by_rules(o['text'], SURN_NATIONAL_RULES)
            if result:
                n += 1
                o['ethnic'] = result[1]
                ncoll.save(o)
        print(n)

    def find_national_names(self):
        fcoll = self._db['fullnames']
        scoll = self._db['surnames']
        ncoll = self._db['names']
        names = {}
        for g in ['ar', ]:
            n = 0
            for o in scoll.find({'ethnic' : g}):
                n += 1
#                print n
                for obj in fcoll.find({'name.sn' : o['text']}):
                    v = names.get(obj['name']['fn'], 0)
                    names[obj['name']['fn']] = v + 1
#                    if obj['name']['fn'] == u'Сергей':
#                        print obj['text']
        thedict = sorted(list(names.items()), key=lambda x, y: x[1], reverse=True)
        print((len(thedict)))
        for n, v in thedict:
            print((n.encode('utf8')))


    def cluster_surnames(self, n=3):
        scoll = self._db['surnames']
        names = {}
        i =0
        for o in scoll.find():
            i += 1
            if i % 10000 == 0:
                print(i)
            if len(o['text']) > n:
                text = o['text'][-n:]
                v = names.get(text, 0)
                names[text] = v + 1
        thedict = sorted(list(names.items()), key=lambda x, y: x[1], reverse=False)
        print((len(thedict)))
        for n, v in thedict:
            print((n.encode('utf8'), v))




    def dump_names(self):
        ncoll = self._db['names']
        for o in ncoll.find().sort('count', -1):
            parts = []
#            parts.append(str(o['count']))
            parts.append(o['text'])
#            parts.append(o['gender'] if o.has_key('gender') else 'n')
            print((('\t'.join(parts))))

    def dump_surnames(self):
        ncoll = self._db['surnames']
        for o in ncoll.find({'f_form' : {'$exists' : False}, 'm_form' : {'$exists' : False}, 'ethnic' : {'$exists' : False}}).sort('count', -1).limit(10000):
            parts = []
            parts.append(str(o['count']))
            parts.append(o['text'])
            parts.append(o['gender'] if 'gender' in o else 'n')
            parts.append(o['text'][-2:])
            print((('\t'.join(parts))))

    def dump_midnames(self):
        ncoll = self._db['midnames']
        for o in ncoll.find().sort('count', -1):
            parts = []
            parts.append(str(o['count']))
            parts.append(o['text'])
            parts.append(o['fname'] if 'fname' in o else '')
            parts.append(o['gender'] if 'gender' in o else 'n')
            print((('\t'.join(parts))))


    def cleanup(self):
        fcoll = self._db['fullnames']
        ncoll = self._db['names']
        mcoll = self._db['midnames']
        scoll = self._db['surnames']
        for o in ncoll.find().sort('count', -1):
            if len(o['text']) == 1 or (len(o['text']) == 2 and o['text'][1] == '.'):
                print((o['text']))
                ncoll.remove(o)
            elif len(o['text']) == 3 and o['text'][1] == '-':
                print((o['text']))
                ncoll.remove(o)
            elif len(o['text']) == 5 and o['text'][1:3] == '.-':
                print((o['text']))
                ncoll.remove(o)
            elif o['text'][0] in ['"', "'"]:
                print((o['text']))
                ncoll.remove(o)
            elif o['text'][-1] in ['"', "'"]:
                print((o['text']))
                ncoll.remove(o)
            else:
                o['lett'] = o['text'][0]
                ncoll.save(o)
        for o in mcoll.find():
            if len(o['text']) == 1 or (len(o['text']) == 2 and o['text'][1] == '.'):
                print((o['text']))
                mcoll.remove(o)
            elif len(o['text']) == 3 and o['text'][1] == '-':
                print((o['text']))
                mcoll.remove(o)
            elif 'gender' in o and o['gender'] == 'u':
                mcoll.remove(o)
            elif o['text'][0] in ['"', "'"]:
                print((o['text']))
                mcoll.remove(o)
            elif o['text'][-1] in ['"', "'"]:
                print((o['text']))
                mcoll.remove(o)
            else:
                o['lett'] = o['text'][0]
                mcoll.save(o)

    def full_valid(self):
        fcoll = self._db['fullnames']
        n = 0
        i = 0
        for o in fcoll.find():
            i += 1
            if i % 10000 == 0:
                print((n, i))
            item = self.parse_name(o['text'])
            if item['parsed']:
                n += 1
                if item['format'] not in ['sfm', 'sf']:
                    print((item['gender'], item['text']))



    def validate(self, filename):
        n = 0
        i = 0
        formats = {}
        for l in open(filename, 'r'):
            i += 1
            if i % 1000 == 0:
                print((n, i, formats))
            l = l.strip().decode('utf8')
            item = self.parse_name(l)
            print((l, item))
            if item['parsed']:
                v = formats.get(item['format'], 0)
                formats[item['format']] = v + 1
#                n += 1
#                if item['gender'] in ['f', 'm', 'u']:
#                    n += 1
                n += 1
#                else:
#                	print item['gender'], item['text']
                pass
#                if item['format'] not in ['sfm', 'sf', 'sFM', 'FMs']:
#                    print item['format'], item['gender'], item['text']
#             else:
#                print item['']
#            else:
#                print item['text']
        print(formats)
        print((n, i))

    def map_surnames_to_names(self):
        ncoll = self._db['names']
        scoll = self._db['surnames']
        for f in ncoll.find({'gender' : 'm'}):
            ma_name = f['text'] + 'ов'
            fe_name = f['text'] + 'ова'
            o = scoll.find_one({'text' : ma_name})
            if o:
                o['fname'] = f['text']
                if 'ethnic' not in o and 'ethnic' in f:
                    o['ethnic'] = f['ethnic']
                scoll.save(o)
                print(ma_name)
            o = scoll.find_one({'text' : fe_name})
            if o:
                o['fname'] = f['text']
                if 'ethnic' not in o and 'ethnic' in f:
                    o['ethnic'] = f['ethnic']
                scoll.save(o)
                print(fe_name)


    def enrich_surnames(self):
        scoll = self._db['surnames']
        for f in scoll.find({'gender' : 'f'}).sort('count', -1):#, 'm_form' : {'$exists' : False}}):
            f_form = f['text']
            m_form = None
            if f['text'][-1] == 'а':
                m_form = f['text'][:-1]
            elif f['text'][-2:] == 'ая':
                m_form = f['text'][:-2] + 'ий'
            if m_form:
                fm = scoll.find_one({'text' : m_form, 'gender' : 'm'})
                if fm:
                    print((f['text']))
                    fm['f_form'] = f['text']
                    scoll.save(fm)
                    f['m_form'] = fm['text']
                    scoll.save(f)

    def stats(self):
        fcoll = self._db['surnames']
        total = 0
        total_n = 0
        n = 0
        tot_n = fcoll.find().count()
        for o in fcoll.find():
            total += o['count']
        for o in fcoll.find().sort('count', -1):
            total_n += o['count']
            n += 1
#            print o['text'].encode('utf8')
            if (float(total_n) / total) > 0.5: break
        print(((float(total_n) / total), n, total_n, tot_n, total))


    def load_ethnic(self):
        f = open('ethnic.txt', 'r')
        fcoll = self._db['names']
        for l in f:
            line = l.strip().decode('utf8')
            parts = line.split('\t')
            if len(parts) != 2: continue
            o = fcoll.find_one({'text': parts[0]})
            if not o: continue
#            if o.has_key('ethnic'): continue
            o['ethnic'] = parts[1].split(',')
            fcoll.save(o)

    def map_ethnic(self):
        fcoll = self._db['names']
        mcoll = self._db['midnames']
        for o in fcoll.find({'ethnic' : {'$exists' : True}}).sort('count', -1):
            all = mcoll.find({'fname' : o['text']})
            for m in all:
                m['ethnic'] = o['ethnic']
                mcoll.save(m)

    def enrich_fullnames(self):
        ncoll = self._db['names']
        mcoll = self._db['midnames']
        scoll = self._db['surnames']
        fcoll = self._db['fullnames']
        i = 0
        for o in fcoll.find({'processed' :{'$exists' : False}}):
            genders = {}
            ethnics = {}
            i += 1
            if i % 1000 == 0: print(i)
            f = ncoll.find_one({'text' : o['name']['fn']})
            if f:
                if 'gender' in f:
                    genders['fn'] = f['gender']
                if 'ethnic' in f:
                    ethnics['fn'] = f['ethnic']
            f = mcoll.find_one({'text' : o['name']['mn']})
            if f:
                if 'gender' in f:
                    genders['mn'] = f['gender']
                if 'ethnic' in f:
                    ethnics['mn'] = f['ethnic']
            f = scoll.find_one({'text' : o['name']['sn']})
            if f:
                if 'gender' in f:
                    genders['sn'] = f['gender']
                if 'ethnic' in f:
                    ethnics['sn'] = f['ethnic']
            o['processed'] = True
            o['genders'] = genders
            o['ethnics'] = ethnics
            fcoll.save(o)

    def get_name_top(self, lett, lett_m):
        ncoll = self._db['names']
        mcoll = self._db['midnames']
        all =  ncoll.find({'lett' : lett[0]}).sort('count', -1).limit(10)
        for o in all:
            print((o['text']))
        all =  mcoll.find({'lett' : lett_m[0]}).sort('count', -1).limit(10)
        for o in all:
            print((o['text']))




    def map_national(self):
        national = 'greek'
        fcoll = self._db['surnames']
        ncoll = self._db['fullnames']
        for f in fcoll.find({'ethnic' : national}):
            print((f['text']))
            all = ncoll.find({'name.sn' : f['text']})
            for o in all:
                print(('-', o['name']['fn'].encode('utf8')))
















def name_recognize():
    """Name recognition"""
    with open('midnames.tsv', 'r') as f:
        i = 0
        n = 0
        for line in f:
            i += 1
            name, num = line.strip().decode('utf8').split('\t')
            if len(name) > 3:
                if name[-2:] == 'ич':
                    gender = 'male'
                    continue
                elif name[-3:] in ['вна', 'чна', 'шна']:
                    gender = 'female'
                    continue
                elif name[-4:] == 'оглы':
                    gender = 'male'
                    continue
                elif name[-4:] == 'кызы':
                    gender = 'female'
                    continue
#                print name[-3:]
                print((name))
                n += 1
        print((n, i))







if __name__ == '__main__':
    np = NamesProcessor()
    np.dump_midnames()

