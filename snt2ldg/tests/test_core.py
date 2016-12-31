# -*- coding: utf-8 -*-

from .context import snt2ldg

import json
import os
import unittest


class SendCoreSnt2LDG(unittest.TestCase):
    """Basic test cases."""

    def test_snt2ldg(self):
        ensnt ="The two of them went to prison and the electric chair respectively."
        desnt = "Obwohl das Wetter schlecht ist, eröffnet die Spiele pünktlich."
        print(os.path.abspath(snt2ldg.__file__))
        ldg = snt2ldg.get_dep_str(desnt, lan='de')
        print(ldg)
        assert len(ldg)> 10


if __name__ == '__main__':
    unittest.main()