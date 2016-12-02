import codecs
import csv
import os
import pickle

from .config_wv import DeBibleCsv
from .config_wv import DeBiblePickle
from .config_wv import EnBiblePickle
from .config_wv import ChBiblePickle


def get_all_lines(fname, encoding='utf8'):
    with codecs.open(fname, "r", encoding) as fd:
        return fd.readlines()


def get_all_rows_from_csv(csvfn, encoding='utf-8'):
    with open(csvfn, 'r') as fb:
        reader = csv.reader(fb)
        return list(reader)


def load_pickle(picklefname):
    psize = os.path.getsize(picklefname)
    if psize > 0:
        with open(picklefname, 'rb') as hp:
            return pickle.load(hp)
    else:
        return {}


def dump_pickle(picklefname, dic):
    with open(picklefname, 'wb') as hp:
        pickle.dump(dic, hp)


def get_bible_pickle(lan=''):
    if lan == 'de':
        with open(DeBiblePickle, 'rb') as hp:
            return pickle.load(hp)
    elif lan == 'ch':
        with open(ChBiblePickle, 'rb') as hp:
            return pickle.load(hp)
    elif lan == 'en':
        with open(EnBiblePickle, 'rb') as hp:
            return pickle.load(hp)
    else:
        print('please set lan=ch|de|en')


def create_bible_raw_snts(fname, encoding='utf8'):
    sntLst = []
    for rowLst in get_all_rows_from_csv(fname, encoding=encoding):
        sntLst.append(rowLst[3])
        sntLst.append('\n')
    path, name = os.path.splitext(fname)
    newfile = path+'.lst'
    with open(newfile, 'w') as fd:
        fd.writelines(sntLst)


if __name__ == "__main__":
    create_bible_raw_snts(DeBibleCsv, encoding='ISO-8859-1')

