# -*- coding: utf-8 -*-

from .context import snt2ldg

import json
import unittest


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


if __name__ == '__main__':
    unittest.main()