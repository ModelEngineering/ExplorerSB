import src.ExplorerSB.constants as cn
from src.ExplorerSB.project import Project
from src.ExplorerSB.project_builder import ProjectBuilder

import pandas as pd
import os
import unittest


IGNORE_TEST = False
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
        self.project = self.makeProject()

    def makeProject(self, project_id=PROJECT_ID):
        project = Project(project_id, data_dir=DATA_DIR)
        project.initialize()
        return project

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertIsNotNone(self.project.project_id)

    def testInitialize(self):
        if IGNORE_TEST:
            return
        Project.PROJECT_DF = None
        self.project.initialize()
        for key in cn.CONTEXT_KEYS:
            self.assertIsNotNone(self.project.__getattribute__(key))
    
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

    def testFindProjectByShortTitle(self):
        if IGNORE_TEST:
            return
        Project.initializeClass()
        short_title = 'Population-based analysis of methadone distribution and metabolism using an age-dependent physiologi...'
        pid = Project.findProjectByShortTitle(short_title)
        project = Project(pid, data_dir=DATA_DIR)
        project.initialize()
        self.assertEqual(project.short_title, short_title)
    
    def testGetFilenames(self):
        if IGNORE_TEST:
            return
        ffiles = self.project.getFilenames(cn.CSV)
        self.assertGreater(len(ffiles), 0)
        some_trues = ["Cl" in n for n in ffiles]
        self.assertTrue(any(some_trues))

    def testGetCSVData(self):
        if IGNORE_TEST:
            return
        filenames = self.project.getFilenames(cn.CSV)
        df = self.project.getCSVData(filenames[0])
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertGreater(len(df), 0)

    def testGetFileContents(self):
        if IGNORE_TEST:
            return
        filenames = self.project.getFilenames(cn.ANT)
        contents = self.project.getFileContents(filenames[0])
        self.assertTrue("comp1" in contents)
    
    def testMakePlotFigure(self):
        if IGNORE_TEST:
            return
        fig = self.project.makePlotFigure()
        if IS_PLOT:
            fig.show()
      
    def testGetModelFiles(self):
        if IGNORE_TEST:
            return
        return
        result = self.project.getModelFiles()

    def testAddJsonFiles(self):
        if IGNORE_TEST:
            return
        return
        generator = Project.iterateProjects()
        for project in generator:
            project.makeJsonData()

if __name__ == '__main__':
    unittest.main()