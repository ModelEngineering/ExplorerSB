from src.ExplorerSB.searcher import Searcher
import src.ExplorerSB.constants as cn

import json
import os
import unittest
import whoosh.index as index


IGNORE_TEST = False
IS_PLOT = False
CITATION_STR = """
summarize the paper
Ana Bulovi\u0107, Stephan Fischer, Marc Dinh, Felipe Golib, Wolfram\
\ Liebermeister, Christian Poirier, Laurent Tournier, Edda Klipp, Vincent\
\ Fromion & Anne Goelzer. Automated generation of bacterial resource allocation\
\ models. Metabolic Engineering 55 (2019): 12-22
"""


#############################
# Tests
#############################
class TestSearcher(unittest.TestCase):

    def setUp(self):
        self.searcher = Searcher()

    def testGet(self):
        if IGNORE_TEST:
            return
        abstract_str = self.searcher.get(CITATION_STR)
        if not cn.IS_GITHUB:
            self.assertGreater(len(abstract_str), 20)
            self.assertTrue("models" in abstract_str)

    def testSearch(self):
        if IGNORE_TEST:
            return
        if cn.IS_GITHUB:
            return
        result_both, _ = self.searcher.search("glycolysis AND pentose")
        result_glc, _ = self.searcher.search("glycolysis")
        result_pen, _ = self.searcher.search("pentose")
        predicted_both = set(result_glc).intersection(result_pen)
        if not cn.IS_GITHUB:
            diff = predicted_both.symmetric_difference(result_both)
            self.assertEqual(len(diff), 0)

    def testGetApikey(self):
        if IGNORE_TEST:
            return
        if cn.IS_GITHUB:
            return
        apikey = self.searcher._getApikey()
        self.assertTrue(isinstance(apikey, str))
        self.assertGreater(len(apikey), 20)


if __name__ == '__main__':
  unittest.main()
