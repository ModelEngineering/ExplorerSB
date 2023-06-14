import src.ExplorerSB.constants as cn
from src.ExplorerSB.corpus_manager import CorpusManager

import os
import unittest


IGNORE_TEST = False
IS_PLOT = False


#############################
# Tests
#############################
class TestCorpusManager(unittest.TestCase):

    def setUp(self):
       self.manager = CorpusManager()

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertGreater(len(self.manager.project_df), 1000)
        self.assertEqual(len(self.manager.project_df), len(self.manager.project_ids))



if __name__ == '__main__':
  unittest.main()