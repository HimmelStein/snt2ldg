# -*- coding: utf-8 -*-

from .context import snt2ldg

import json
import unittest

table_kdic = [
    {"lan": "de",  "table": "pons",  "snt": "de_snt",  "ldg": "de_ldg"},
    {"lan": "ch", "table": "pons", "snt": "ch_snt", "ldg": "ch_ldg"},
    {"lan": "ch", "table": "ldc2002t01", "snt": "ch_snt", "ldg": "ch_ldg"},
    {"lan": "en",  "table": "ldc2002t01", "snt": "en_snt",  "ldg": "en_ldg"},
    {"lan": "de", "table": "debible", "snt": "snt", "ldg": "snt_lg"},
    {"lan": "ch", "table": "chbible", "snt": "snt", "ldg": "snt_lg"},
    {"lan": "en", "table": "enbible", "snt": "snt", "ldg": "snt_lg"},
    ]

class TestDatabase(unittest.TestCase):
    """Basic test cases."""

    def test_database_existancy(self):
        dbnames = ['postgres://localhost/language_graph',
                   'sqlite:///data/PONS.db']
        for dbname in dbnames:
            n = snt2ldg.check_database(dbname)
            print(dbname, n)
            assert n > 0

    def test_get_ldg_from_pons(self):
        refLst = [("ch", 1, "0 他 _ _ r _ 1 SBV _ _ _ * 1 导演 _ _ v _ -1 HED _ _ _ * 2 了 _ _ u _ 1 RAD _ _ _ * 3 那场 _ _ r _ 4 ATT _ _ _ * 4 话剧 _ _ n _ 1 VOB _ _ _ * 5 。 _ _ wp _ 1 WP _ _ _"),
                  ("de", 1, '1 Er er PRO PPER 3|Sg|Masc|Nom 2 subj _ _  * 2 hat haben V VAFIN 3|Sg|Pres|Ind 0 root _ _  * 3 bei bei PREP APPR Dat 2 pp _ _  * 4 jenem jene ART PDAT _|Dat|Sg 5 det _ _  * 5 Theater Theater N NN Fem|Dat|Sg 3 pn _ _  * 6 Regie Regie N NN Fem|Dat|Sg 5 app _ _  * 7 geführt führen V VVPP _ 2 aux _ _  * 8 . . $. $. _ 0 root _ _  *  * ')
               ]
        for lan, id, ref in refLst:
            ldg = snt2ldg.get_raw_ldg_with_id_from_pons(id, lan=lan)
            print(ldg)
            assert ref == ldg

    def test_sample_ldg_from_table(self):
        refLst = [(0, "pons", "ch", "0 我 _ _ r _ 1 SBV _ _ _ * 1 是 _ _ v _ -1 HED _ _ _ * 2 德国 _ _ ns _ 3 ATT _ _ _ * 3 人 _ _ n _ 1 VOB _ _ _ * 4 。 _ _ wp _ 1 WP _ _ _"),
                  (1, "pons", "de", "1 Hans Hans N NE Masc|Nom|Sg 4 subj _ _  * 2 und und KON KON _ 1 kon _ _  * 3 Anna Anna N NE Fem|Nom|Sg 2 cj _ _  * 4 spielen spielen V VVFIN _|Pl|Pres|_ 0 root _ _  * 5 gerade gerade ADV ADV _ 4 adv _ _  * 6 Schach Schach N NN Neut|_|Sg 4 obja _ _  * 7 . . $. $. _ 0 root _ _  *  * "),
                  (10,"ldc2002t01", "en", "1 The _ DT DT _ 4 det _ _ * 2 ASEAN _ NNP NNP _ 4 compound _ _ * 3 summit _ NN NN _ 4 compound _ _ * 4 meeting _ NN NN _ 15 nsubj _ _ * 5 held _ VBN VBN _ 4 acl _ _ * 6 in _ IN IN _ 7 case _ _ * 7 Hanoi _ NNP NNP _ 5 nmod _ _ * 8 in _ IN IN _ 10 case _ _ * 9 the _ DT DT _ 10 det _ _ * 10 middle _ NN NN _ 5 nmod _ _ * 11 of _ IN IN _ 13 case _ _ * 12 this _ DT DT _ 13 det _ _ * 13 month _ NN NN _ 10 nmod _ _ * 14 has _ VBZ VBZ _ 15 aux _ _ * 15 decided _ VBN VBN _ 0 root _ _ * 16 to _ TO TO _ 17 mark _ _ * 17 accept _ VB VB _ 15 xcomp _ _ * 18 Cambodia _ NNP NNP _ 17 dobj _ _ * 19 as _ IN IN _ 22 case _ _ * 20 its _ PRP$ PRP$ _ 22 nmod:poss _ _ * 21 tenth _ JJ JJ _ 22 amod _ _ * 22 member _ NN NN _ 18 nmod _ _ * 24 and _ CC CC _ 15 cc _ _ * 25 has _ VBZ VBZ _ 26 aux _ _ * 26 authorized _ VBN VBN _ 15 conj _ _ * 27 ASEAN _ NNP NNP _ 29 compound _ _ * 28 Foreign _ NNP NNP _ 29 compound _ _ * 29 Ministers _ NNP NNP _ 26 dobj _ _ * 30 to _ TO TO _ 31 mark _ _ * 31 prepare _ VB VB _ 26 xcomp _ _ * 32 the _ DT DT _ 33 det _ _ * 33 ceremony _ NN NN _ 31 dobj _ _ * 34 in _ IN IN _ 35 case _ _ * 35 Hanoi _ NNP NNP _ 33 nmod _ _ * 36 to _ TO TO _ 38 mark _ _ * 37 officially _ RB RB _ 38 advmod _ _ * 38 welcome _ VB VB _ 31 advcl _ _ * 39 Cambodia _ NNP NNP _ 38 dobj _ _ * 40 to _ TO TO _ 41 mark _ _ * 41 join _ VB VB _ 38 xcomp _ _ * 42 ASEAN _ NNP NNP _ 41 dobj _ _ * "),
                  (1000, "debible", "de", "1 und und KON KON _ 0 root _ _  * 2 die die ART ART Def|_|_|_ 1 cj _ _  * 3 ihnen sie PRO PPER 3|Pl|_|Dat 0 root _ _  * 4 Unrecht Unrecht N NN Neut|_|Sg 5 obja _ _  * 5 taten tun V VVFIN _|Pl|Past|Ind 0 root _ _  * 6 , , $, $, _ 0 root _ _  * 7 waren sein V VAFIN _|Pl|Past|Ind 5 kon _ _  * 8 zu zu PTKA PTKA _ 9 adv _ _  * 9 mächtig mächtig ADV ADJD Pos| 7 pred _ _  * 10 , , $, $, _ 0 root _ _  * 11 dass dass KOUS KOUS _ 16 konj _ _  * 12 sie sie PRO PPER 3|Pl|_|Nom 16 subj _ _  * 13 keinen keine ART PIAT Masc|Acc|Sg 14 det _ _  * 14 Tröster Tröster N NN Masc|Acc|Sg 16 obja _ _  * 15 haben haben V VAINF _ 16 aux _ _  * 16 konnten können V VMFIN 3|Pl|Past|Ind 7 objc _ _ "),                  (100, "enbible", "en", "1 And _ CC CC _ 3 cc _ _ * 2 they _ PRP PRP _ 3 nsubj _ _ * 3 said _ VBD VBD _ 21 ccomp _ _ * 4 to _ TO TO _ 5 case _ _ * 5 him _ PRP PRP _ 3 nmod _ _ * 7 Where _ WRB WRB _ 8 advmod _ _ * 8 is _ VBZ VBZ _ 3 dep _ _ * 9 Sarah _ NNP NNP _ 8 nsubj _ _ * 10 your _ PRP$ PRP$ _ 11 nmod:poss _ _ * 11 wife _ NN NN _ 9 dep _ _ * 13 And _ CC CC _ 3 cc _ _ * 14 he _ PRP PRP _ 15 nsubj _ _ * 15 said _ VBD VBD _ 3 conj _ _ * 17 She _ PRP PRP _ 21 nsubj _ _ * 18 is _ VBZ VBZ _ 21 cop _ _ * 19 in _ IN IN _ 21 case _ _ * 20 the _ DT DT _ 21 det _ _ * 21 tent _ NN NN _ 0 root _ _ * "),
                  (99999, "pons", "ch", "")]
        for id, tb, lan, ref in refLst:
            ldg = snt2ldg.sample_snt_to_ldg_in_table(id, table=tb, lan=lan)
            print(ldg)
            print(len(ldg), len(ref))
            assert ldg == ref

    # def test_load_pickle_to_db(self):
    #        num = snt2ldg.load_bible_ldg_into_table_from_pickle(lans=['de'])
    #        assert num > 0

if __name__ == '__main__':
    unittest.main()