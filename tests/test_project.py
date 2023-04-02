import src.ExplorerSB.util as util
import src.ExplorerSB.constants as cn
import src.ExplorerSB.project as pjt

import os
import unittest


IGNORE_TEST = False
IS_PLOT = False
PROJECT_ID = "iYS854"



#############################
# Tests
#############################
class TestProjects(unittest.TestCase):

    def setUp(self):
        self.project = pjt.Project(PROJECT_ID)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        import pdb; pdb.set_trace()



if __name__ == '__main__':
  unittest.main()
