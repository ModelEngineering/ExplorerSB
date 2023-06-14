import src.ExplorerSB.constants as cn
from src.ExplorerSB.project_reader import Project
from src.ExplorerSB.project_builder import ProjectBuilder

import pandas as pd
import os
import unittest


IGNORE_TEST = True
IS_PLOT = False
PROJECT_ID = "Yeast-cell-cycle-Irons-J-Theor-Biol-2009"
PROJECT_RUNID = "61fea483f499ccf25faafc4d"
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DATA_DIR, "test_data")
CONTEXT_FILE = os.path.join(DATA_DIR, "test_context.csv")


#############################
# Tests
#############################
class TestProject(unittest.TestCase):

    def setUp(self):
        self.project = Project(PROJECT_ID, data_dir=DATA_DIR)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertIsNotNone(self.project.project_id)
        import pdb; pdb.set_trace()

    def testIterateProjects(self):
        if IGNORE_TEST:
            return
        def test(projects, expected_length):
            self.assertEqual(len(projects), expected_length)
            if len(projects) > 0:
                self.assertTrue(isinstance(projects[0], Project))
        #
        projects = [p for p in Project.iterateProjects()]
        test(projects, len(Project.PROJECT_IDS))
        #
        projects = [p for p in Project.iterateProjects(first=2, last=2)]
        test(projects, 1)
        #
        ignored_project_ids = Project.PROJECT_IDS
        projects = [p for p in 
                    Project.iterateProjects(ignored_project_ids=ignored_project_ids)]
        test(projects, 0)
    
    def testListFiles(self):
        if IGNORE_TEST:
            return
        ffiles = self.project.listFiles()
        self.assertGreater(len(ffiles), 0)

    def testGetFile(self):
        if IGNORE_TEST:
            return
        pass

if __name__ == '__main__':
    unittest.main()