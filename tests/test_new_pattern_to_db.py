# -*- coding: utf-8 -*-

from .context import snt2ldg
from nltk.parse import DependencyGraph
from copy import deepcopy
from pprint import pprint

import json
import unittest



class SendCoreSnt2LDG(unittest.TestCase):
    """Basic test cases."""

    @unittest.skip("skipping")
    def test_make_word_list_from_phrase(self):
        lst = [("not only...but also", ["not", "only", "but", "also"]),
               ("Weder...noch..", ["Weder", "noch"])]
        for pair in lst:
            wlst = snt2ldg.make_word_list_from_phrase(pair[0])
            print(wlst)
            assert wlst == pair[1]

    @unittest.skip("skipping")
    def test_dependency_graph(self):
        lst = [
            ("Weder war der Stern von Bethlehem eine Supernova, noch  ein Komet.  ",
                "1	Weder	_	NNP	NNP	_	6	compound	_	_*\
2	war	_	NN	NN	_	6	compound	_	_*\
3	der	_	NN	NN	_	6	compound	_	_*\
4	Stern	_	NNP	NNP	_	6	compound	_	_*\
5	von	_	NNP	NNP	_	6	compound	_	_*\
6	Bethlehem	_	NNP	NNP	_	7	nsubj	_	_*\
7	eine	_	VBP	VBP	_	0	root	_	_*\
8	Supernova	_	NNP	NNP	_	12	compound	_	_*\
10	noch	_	NNP	NNP	_	12	appos	_	_*\
11	ein	_	NNPS	NNPS	_	12	compound	_	_*\
12	Komet	_	NNP	NNP	_	7	dobj	_	_*")]
        for pair in lst:
            cnll = snt2ldg.get_dep_str(pair[0])
            cnll = cnll.replace('\n','*')
            print('cnll', cnll)
            print(len(cnll), len(pair[1]))
            assert cnll == pair[1]

    @unittest.skip('')
    def test_minimal_connected_graph(self):
        lst = [
            (
            "1 Nero _ NNP NNP _ 2 nsubj _ _ *2 played _ VBD VBD _ 0 root _ _ *3 his _ PRP$ PRP$ _ 4 nmod:poss _ _ *4 flute _ NN NN _ 2 dobj _ _ *5 while _ IN IN _ 7 mark _ _ *6 Rome _ NNP NNP _ 7 nsubj _ _ *7 burned _ VBD VBD _ 2 advcl _ _ *",
            ["while"], [2], [7],[5,7,2]),
            ("1	Weder	_	NNP	NNP	_	6	compound	_	_*\
2	war	_	NN	NN	_	6	compound	_	_*\
3	der	_	NN	NN	_	6	compound	_	_*\
4	Stern	_	NNP	NNP	_	6	compound	_	_*\
5	von	_	NNP	NNP	_	6	compound	_	_*\
6	Bethlehem	_	NNP	NNP	_	7	nsubj	_	_*\
7	eine	_	VBP	VBP	_	0	root	_	_*\
8	Supernova	_	NNP	NNP	_	12	compound	_	_*\
10	noch	_	NNP	NNP	_	12	appos	_	_*\
11	ein	_	NNPS	NNPS	_	12	compound	_	_*\
12	Komet	_	NNP	NNP	_	7	dobj	_	_*", ["Weder", "noch"], [7], [6, 12],[1, 6, 10, 12, 7])
               ]
        for record in lst:
            cnll = record[0]
            cnll = cnll.replace('*', '\n')
            g = DependencyGraph(cnll)
            root = snt2ldg.get_root_address_from_nltkg(g)
            print('root', root)
            assert root == record[2]

            newg = deepcopy(g)
            addressLst = []
            rootAddress = snt2ldg.get_root_address_from_nltkg(newg)
            wordAddress = []
            for word in record[1]:
                wordAddress +=  snt2ldg.get_address_of_word(newg, word)
            for address in wordAddress:
                 addressBetween = snt2ldg.get_addresses_from_child_to_ancestor(newg, address, rootAddress[0])
                 addressLst += [address] + addressBetween

            addressLst+=rootAddress
            print(addressLst)
            assert addressLst == record[4]
            for i in list(newg.nodes.keys()):
                if i not in addressLst:
                    newg.remove_by_address(i)
            pprint(newg.nodes)
            assert len(newg.nodes) == len(record[4])

    @unittest.skip("skipping")
    def test_create_conjunction_pattern(self):
        testLst = [
             ("aber","Die Sonne ist nicht sehr groß,aber sie ist heiß.  ",
             "de",
              "3 sein V VAFIN 3|Sg|Pres|Ind 0 root ist  _ _ *8 aber KON KON _ 3 kon aber  _ _ *",
              "0 None TOP TOP None None None None  _ _ *1 die ART ART Def|Fem|Nom|Sg 2 det Die  _ _ *2 Sonne N NN Fem|Nom|Sg 3 subj Sonne  _ _ *3 sein V VAFIN 3|Sg|Pres|Ind 0 root ist  _ _ *4 nicht PTKNEG PTKNEG _ 3 adv nicht  _ _ *5 sehr ADV ADV _ 6 adv sehr  _ _ *6 groß ADV ADJD Pos| 3 pred groß  _ _ *7 , $, $, _ 0 root ,  _ _ *8 aber KON KON _ 3 kon aber  _ _ *9 sie PRO PPER 3|Sg|Fem|Nom 10 subj sie  _ _ *10 sein V VAFIN 3|Sg|Pres|Ind 8 cj ist  _ _ *11 heiß ADV ADJD Pos| 10 pred heiß  _ _ *12 . $. $. _ 0 root .  _ _ *"),
            ("Weder...noch..",
             "Weder war der Stern von Bethlehem eine Supernova, noch  ein Komet.  ",
             "de",
             "1 weder KON KON _ 2 koord Weder  _ _ *2 sein V VAFIN 3|Sg|Past|Ind 0 root war  _ _ *10 noch KON KON _ 0 root noch  _ _ *",
             "0 None TOP TOP None None None None  _ _ *1 weder KON KON _ 2 koord Weder  _ _ *2 sein V VAFIN 3|Sg|Past|Ind 0 root war  _ _ *3 die ART ART Def|Masc|Nom|Sg 4 det der  _ _ *4 Stern N NN Masc|Nom|Sg 2 subj Stern  _ _ *5 von PREP APPR Dat 4 pp von  _ _ *6 Bethlehem N NE Neut|Dat|Sg 5 pn Bethlehem  _ _ *7 eine ART ART Indef|Fem|Nom|Sg 8 det eine  _ _ *8 Supernova N NN Fem|Nom|Sg 2 pred Supernova  _ _ *9 , $, $, _ 0 root ,  _ _ *10 noch KON KON _ 0 root noch  _ _ *11 eine ART ART Indef|Masc|Nom|Sg 12 det ein  _ _ *12 Komet N NN Masc|Nom|Sg 10 cj Komet  _ _ *13 . $. $. _ 0 root .  _ _ *"),
            (
                "and",
                "The two of them went to prison and the electric chair respectively.",
                "en",
                "5 went VBD VBD _ 0 root _ _ _ *7 prison NN NN _ 5 nmod _ _ _ *8 and CC CC _ 7 cc _ _ _ *",
                "0 None TOP TOP None None None None _ _ *1 The DT DT _ 2 det _ _ _ *2 two CD CD _ 5 nsubj _ _ _ *3 of IN IN _ 4 case _ _ _ *4 them PRP PRP _ 2 nmod _ _ _ *5 went VBD VBD _ 0 root _ _ _ *6 to TO TO _ 7 case _ _ _ *7 prison NN NN _ 5 nmod _ _ _ *8 and CC CC _ 7 cc _ _ _ *9 the DT DT _ 11 det _ _ _ *10 electric JJ JJ _ 11 amod _ _ _ *11 chair NN NN _ 7 conj _ _ _ *12 respectively RB RB _ 5 advmod _ _ _ *"
            )
        ]
        for pair in testLst:
            cnll, cnll1=snt2ldg.create_conjunction_pattern(pair[0], pair[1], lan=pair[2])
            cnll = cnll.replace('\n', '*')
            cnll1 = cnll1.replace('\n', '*')
            print(cnll)
            print(pair[3])
            print(cnll1)
            print(pair[4])
            assert cnll == pair[3]
            assert cnll1 == pair[4]

    def test_query_db(self):
        queryLst = [("postgres://localhost/language_graph","select en_words from ed_words group by en_words;", "partly...partly"),
                    ("postgres://localhost/language_graph", "select en_snt, de_snt  from ed_snt;",
                     "Einstein was a clean person, but he never combed his hair.")
        ]
        for records in queryLst:
            rlt = sum(snt2ldg.get_query_result_from_db(records[0], records[1]),[])
            print(rlt)
            assert records[2] in rlt

    def test_is_valid_phrase(self):
        refLst=[
            ("partly...partly", "partly a b c d, partly e f sdfas .")
        ]
        for records in refLst:
            assert snt2ldg.is_valid_sample(records[0], records[1])

    # @unittest.skip('skip this')
    def test_learn_en_phrase_patterns(self):
        databaseName = "postgres://localhost/language_graph"
        phraseQueryEn  = "select en_words from ed_words group by en_words;"
        sampleQueryEnDe = "select en_snt, de_snt  from ed_snt;"
        queryFormatEn = """INSERT INTO en_pat VALUES({0}, '{1}', '{2}', '{3}', '{4}', {5})"""
        count = snt2ldg.learn_phrase_patterns(lan='en', database=databaseName, phraseQuery=phraseQueryEn,
                                      sampleQuery=sampleQueryEnDe, queryFormat=queryFormatEn)
        print(count)
        assert count > 0

    # @unittest.skip('skip this')
    def test_learn_de_phrase_patterns(self):
        databaseName = "postgres://localhost/language_graph"
        phraseQueryEn = "select de_words from ed_words group by de_words;"
        sampleQueryEnDe = "select en_snt, de_snt  from ed_snt;"
        queryFormatEn = """INSERT INTO de_pat VALUES({0}, '{1}', '{2}', '{3}', '{4}', {5})"""
        count = snt2ldg.learn_phrase_patterns(lan='de', database=databaseName, phraseQuery=phraseQueryEn,
                                              sampleQuery=sampleQueryEnDe, queryFormat=queryFormatEn)
        print(count)
        assert count > 0

    def test_get_root_of_node(self):
        assert True


if __name__ == '__main__':
    unittest.main()

