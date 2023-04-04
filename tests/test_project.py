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

    def testGetFileUrls(self):
        if IGNORE_TEST:
            return
        result = self.project.cacheFiles()
        self.assertGreater(len(result), 0)
        self.assertTrue(isinstance(result[0], str))

    def testGetProjectIds(self):
        if IGNORE_TEST:
            return
        def test(result):
            self.assertGreater(len(result), 0)
            self.assertTrue(isinstance(result[0], str))
        #
        self.assertIsNone(self.project.project_ids)
        test(self.project.getProjectIds())
        self.assertIsNotNone(self.project.project_ids)
        test(self.project.getProjectIds())
    



if __name__ == '__main__':
  unittest.main()
