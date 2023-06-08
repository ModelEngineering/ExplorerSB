import src.ExplorerSB.util as util
import src.ExplorerSB.constants as cn
import src.ExplorerSB.summary_parser as sp

import os
import unittest


IGNORE_TEST = False
IS_PLOT = False
PROJECT_IDS = ["Yeast-cell-cycle-Irons-J-Theor-Biol-2009",
               "EGF-TNFa-signaling-Chaouiya-BMC-Syst-Biol-2013",
               "Escherichia-coli-core-metabolism-textbook",
               "Escherichia-coli-resource-allocation-Bulovic-Metab-Eng-2019",
               "HSP-synthesis-Szymanska-J-Theor-Biol-2009",
               "Hodgkin-Huxley-cell-Gleeson"]
TEST_FILES = [os.path.join(cn.TEST_DIR, "summary%d.txt" % n) for n in [1, 2]]
SUMMARIES = []
for ffile in TEST_FILES:
    with open(ffile, "r") as fd:
        line = fd.readline()
        if line[-1] == "\n":
            line = line[:-1]
        line_as_bytes = bytes(line, 'utf-8')
        SUMMARIES.append(line_as_bytes)


#############################
# Tests
#############################
class TestBiosimulationsSummaryParser(unittest.TestCase):

    def setUp(self):
        self.parsers = [sp.BiosimulationsSummaryParser(id, is_report=False) for id in PROJECT_IDS]
        [p._initialize() for p in self.parsers]

    def testConstructor(self):
        if IGNORE_TEST:
            return
        for parser in self.parsers:
            self.assertTrue(isinstance(parser.summary_dct, dict))

    def testGetPaperUrl(self):
        if IGNORE_TEST:
            return
        for parser in self.parsers:
            paper_url, error_str = parser._getPaperUrl()
            self.assertGreater(len(paper_url), 0)
            self.assertEqual(len(error_str), 0)

    def testExtractDoi(self):
        if IGNORE_TEST:
            return
        def test(idx):
            parser = self.parsers[idx]
            doi, error_str = parser._extractDOI()
            self.assertGreater(len(doi), 0)
            self.assertEqual(len(error_str), 0)
        #
        test(0)
        test(1)

    def testExtractCitation(self):
        if IGNORE_TEST:
            return
        def test(idx):
            parser = self.parsers[idx]
            citation, error_str = parser._extractCitation()
            self.assertGreater(len(citation), 0)
            self.assertEqual(len(error_str), 0)
        #
        test(0)
        test(1)

    def testGetAbstract(self):
        if IGNORE_TEST:
            return
        def test(project_id):
            parser = sp.BiosimulationsSummaryParser(project_id, is_report=True)
            parser._initialize()
            doi, _ = parser._extractDOI()
            citation, _ = parser._extractCitation()
            parser.do()
            abstract = parser._getAbstract(doi, citation)
            self.assertGreater(len(abstract), 0)
        #
        test(PROJECT_IDS[0])

    def testDo(self):
        if IGNORE_TEST:
            return
        def test(idx):
            parser = self.parsers[idx]
            parser.do()
            attributes = ["citation", "title", "abstract", "doi"]
            for attribute in attributes:
                value = parser.__getattribute__(attribute)
                if len(value) == 0:
                    if attribute == "abstract":
                        continue
                self.assertGreater(len(value), 0)
        #
        test(0)
        test(1)

if __name__ == '__main__':
  unittest.main()