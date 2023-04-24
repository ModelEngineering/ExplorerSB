import src.ExplorerSB.constants as cn
from src.ExplorerSB.project_base import ProjectBase

import os
import pandas as pd
import shutil
import unittest
import urllib3


IGNORE_TEST = False
PROJECT_ID = "Yeast-cell-cycle-Irons-J-Theor-Biol-2009"
RUNID = "runid"
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DATA_DIR, "test_data")
RUNID = "runid"
PROJECT_CACHE_DIR = os.path.join(DATA_DIR, RUNID)
PROJECT_FILE = os.path.join(PROJECT_CACHE_DIR, "dummy.txt")


#############################
# Tests
#############################
class TestProject(unittest.TestCase):

    @staticmethod
    def removeProjectDirectory():
        path = os.path.join(DATA_DIR, RUNID)
        if os.path.isdir(path):
            shutil.rmtree(path)
    
    @classmethod
    def setUpClass(self):
        self.removeProjectDirectory()

    @classmethod
    def tearDownClass(self):
        self.removeProjectDirectory()

    def setUp(self):
        self.project = ProjectBase(PROJECT_ID, data_dir=DATA_DIR)
        self.project.runid = RUNID

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertIsNotNone(self.project.project_id)

    def testGetProjectCacheDirectory(self):
        if IGNORE_TEST:
            return
        path = self.project.getProjectCacheDirectory(is_create=True)
        self.assertTrue(os.path.isdir(path))
     
    def testGetFilePaths(self):
        if IGNORE_TEST:
            return
        ffiles = self.project.getFilePaths(is_create=False)
        self.assertEqual(len(ffiles), 0)
        #
        ffiles = self.project.getFilePaths(is_create=True)
        with open(PROJECT_FILE, "w") as fd:
            fd.writelines("testing")
        ffiles = self.project.getFilePaths(is_create=False)
        self.assertTrue(PROJECT_FILE in ffiles)


if __name__ == '__main__':
    unittest.main()