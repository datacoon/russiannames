# -*- coding: UTF-8 -*-

import sys, os.path


class NameReader:
    def __init__(self, path):
        self.path = path
        self.names = {}
        self.surnames = {}
        self.midnames  = {}
        self.n = 0
        self.f_all = open('all.txt', 'w')
        self.f_o = open('not3.txt', 'w')


    def process(self):
        dirs = os.listdir(self.path)
        for d in dirs:
            self.process_dir(os.path.join(self.path, d))

    def process_dir(self, dirname):
        files = os.listdir(dirname)
        for fname in files:
            filename = os.path.join(dirname, fname)
            f = open(filename)
            lines = f.read().splitlines()
            f.close()
            for line in lines:
                parts = line.split()
                if len(parts) != 3:
                    self.f_o.write(line.encode('utf8') + '\n')
                    self.n += 1
                else:
                    (surname, name, midname) = parts
                    v = self.names.get(name, 0)
                    self.names[name] = v + 1
                    v = self.surnames.get(surname, 0)
                    self.surnames[surname] = v + 1
                    v = self.midnames.get(midname, 0)
                    self.midnames[midname] = v + 1
                    self.f_all.write(line.encode('utf8') + '\n')

    def write_dict(self, dict, filename):
        f = open(filename, 'w')
        thedict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        for key, value in thedict:
            f.write(('%s\t%d' %(key, value)).encode('utf8') + '\n')



    def save(self):
        self.write_dict(self.names, 'names.tsv')
        self.write_dict(self.surnames, 'surnames.tsv')
        self.write_dict(self.midnames, 'midnames.tsv')


def name_parse(dirname):
    reader = NameReader(dirname)
    reader.process()
    reader.save()
    print(reader.n)
    print(len(reader.names.keys()), len(reader.midnames.keys()), len(reader.surnames.keys()))
    thedict = sorted(reader.names.items(), lambda x, y: x[1], reverse=True)
    for key, value in thedict[00:50]:
        print(value, key.encode('utf8'))





if __name__ == '__main__':
    name_parse(sys.argv[1])
