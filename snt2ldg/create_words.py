
from .pickle_util import load_pickle, get_all_rows_from_csv
from .config_wv import EnBibleCsv, EnBiblePickle, EnBibleWords


#
# input csv and pickle which save sentences and langauge dependency graphs of a book, here, bible
# output a text each line is word in the text
# in German version, punctuations are started with $ in dependency graph
# in Chinese version, punctuations are marked with wp in dependency graph
# in English version, all punctuations are ignored.
#

def generate_word_list_from_book(inputcsv, inputpickle, outputtxt, encoding='utf-8', ignore=[]):
    """
    :param inputcsv: filename, book in csv form, each line is a sentence
    :param inputpickle: filename, book in pickle form, each index points to the dependency graph of the sentence
    :param outputtxt: filename, word list, all punctuations are ignored.
    :return:
    """
    dic =  load_pickle(inputpickle)
    words = []
    allRowLst =  get_all_rows_from_csv(inputcsv, encoding=encoding)

    for i in range(len(allRowLst)):
        rowLst = allRowLst[i]
        key = rowLst[0] + "_" + "_" + rowLst[1] + "_" + rowLst[2]
        snt = rowLst[3]
        if len(snt.strip()) == 0:
            continue
        else:
            ldg = dic.get(key, '')
            print(key)
            print(ldg)


if __name__ == "__main__":
    generate_word_list_from_book(EnBibleCsv, EnBiblePickle, EnBibleWords)
