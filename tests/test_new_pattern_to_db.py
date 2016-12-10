# -*- coding: utf-8 -*-

from .context import snt2ldg
from nltk.parse import DependencyGraph
from copy import deepcopy
from pprint import pprint

import json
import unittest



class SendCoreSnt2LDG(unittest.TestCase):
    """Basic test cases."""

    def test_make_word_list_from_phrase(self):
        lst = [("not only...but also", ["not", "only", "but", "also"]),
               ("Weder...noch..", ["Weder", "noch"])]
        for pair in lst:
            wlst = snt2ldg.make_word_list_from_phrase(pair[0])
            print(wlst)
            assert wlst == pair[1]

    def test_dependency_graph(self):
        lst = [("Weder war der Stern von Bethlehem eine Supernova, noch  ein Komet.  ",
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
            print(cnll)
            print(len(cnll), len(pair[1]))
            assert cnll == pair[1]

    def test_minimal_connected_graph(self):
        lst = [("1	Weder	_	NNP	NNP	_	6	compound	_	_*\
2	war	_	NN	NN	_	6	compound	_	_*\
3	der	_	NN	NN	_	6	compound	_	_*\
4	Stern	_	NNP	NNP	_	6	compound	_	_*\
5	von	_	NNP	NNP	_	6	compound	_	_*\
6	Bethlehem	_	NNP	NNP	_	7	nsubj	_	_*\
7	eine	_	VBP	VBP	_	0	root	_	_*\
8	Supernova	_	NNP	NNP	_	12	compound	_	_*\
10	noch	_	NNP	NNP	_	12	appos	_	_*\
11	ein	_	NNPS	NNPS	_	12	compound	_	_*\
12	Komet	_	NNP	NNP	_	7	dobj	_	_*", ["Weder", "noch"], [7], [6, 12])]
        for record in lst:
            cnll = record[0]
            cnll = cnll.replace('*', '\n')
            g = DependencyGraph(cnll)
            root = snt2ldg.get_root_address_from_nltkg(g)
            print('root', root)
            assert root == record[2]
            lst1 = snt2ldg.get_addresses_from_child_to_ancestor(g, 1, 7, stop=[7])
            print('lst1', lst1)
            assert [6 ]== lst1 and len(lst1) == 1
            lst2 = snt2ldg.get_addresses_from_child_to_ancestor(g, 10, 7,  stop=[7])
            print('lst2', lst2)
            assert [12] == lst2 and len(lst2) == 1

            newg = deepcopy(g)
            addressLst = []
            rootAddress = snt2ldg.get_root_address_from_nltkg(newg)
            wordAddress = [1,10]
            for address in wordAddress:
                 addressBetween = snt2ldg.get_addresses_from_child_to_ancestor(newg, address, rootAddress[0])
                 addressLst += [address] + addressBetween

            addressLst+=rootAddress
            print(addressLst)
            assert addressLst == [1, 6, 10, 12, 7]
            for i in list(newg.nodes.keys()):
                if i not in addressLst:
                    newg.remove_by_address(i)
            pprint(newg.nodes)
            assert len(newg.nodes) == 5

            address1 = snt2ldg.get_children_addresses(g, 1)
            print('address1', address1)
            assert address1 == []

            address2 = snt2ldg.get_children_addresses(g, 10)
            print('address2', address2)
            assert address2 == []


    @unittest.skip("skipping")
    def test_create_conjunction_pattern(self):
        testLst = [
             ("aber","Die Sonne ist nicht sehr groß,aber sie ist heiß.  ",
             "de",
              "3 sein V VAFIN 3|Sg|Pres|Ind 0 root  _ _ *8 aber KON KON _ 3 kon  _ _ *",
              "3 sein V VAFIN 3|Sg|Pres|Ind 0 root  _ _ *8 aber KON KON _ 3 kon  _ _ *10 sein V VAFIN 3|Sg|Pres|Ind 8 cj  _ _ *"),
            ("Weder...noch..",
             "Weder war der Stern von Bethlehem eine Supernova, noch  ein Komet.  ",
             "de",
             "1 weder KON KON _ 2 koord  _ _ *2 sein V VAFIN 3|Sg|Past|Ind 0 root  _ _ *10 noch KON KON _ 0 root  _ _ *",
             "1 weder KON KON _ 2 koord  _ _ *2 sein V VAFIN 3|Sg|Past|Ind 0 root  _ _ *10 noch KON KON _ 0 root  _ _ *")
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

    def test_learn_phrase_patterns(self):
        databaseName = "postgres://localhost/language_graph"
        phraseQueryEn  = "select de_words from ed_words group by de_words;"
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

