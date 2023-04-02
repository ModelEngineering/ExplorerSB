import src.ExplorerSB.util as util
import src.ExplorerSB.constants as cn
import src.ExplorerSB.project as pjt

import os
import unittest


IGNORE_TEST = True
IS_PLOT = True
PROJECT_ID = "iYS854"
PROJECT_ID = "Yeast-cell-cycle-Irons-J-Theor-Biol-2009"



#############################
# Tests
#############################
class TestProjects(unittest.TestCase):

    def setUp(self):
        self.project = pjt.Project(PROJECT_ID)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertGreater(len(self.project.summary_dct), 0)

    # TODO: finish
    def testGetFileUrls(self):
        # TESTING
        result = self.project.cacheFiles()
        import pdb; pdb.set_trace()



if __name__ == '__main__':
  unittest.main()
