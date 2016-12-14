# -*- coding: utf-8 -*-

from .context import snt2ldg

import json
import unittest


class SendCoreSnt2LDG(unittest.TestCase):
    """Basic test cases."""

    def test_snt2ldg(self):
        ensnt ="The two of them went to prison and the electric chair respectively."
        ldg = snt2ldg.get_dep_str(ensnt, lan='en')
        print(ldg)
        assert True


if __name__ == '__main__':
    unittest.main()