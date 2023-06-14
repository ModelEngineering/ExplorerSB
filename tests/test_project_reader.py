import src.ExplorerSB.constants as cn
from src.ExplorerSB.project_reader import ProjectReader
from src.ExplorerSB.project_builder import ProjectBuilder
from src.ExplorerSB.corpus_manager import CorpusManager

import pandas as pd
import os
import unittest


IGNORE_TEST = False
IS_PLOT = False
PROJECT_ID = "Yeast-cell-cycle-Irons-J-Theor-Biol-2009"
PROJECT_RUNID = "61fea483f499ccf25faafc4d"
DATA_DIR = cn.DATA_DIR
PROJECT_FILE = "report_del_Cln2.csv"
CORPUS_MANAGER = CorpusManager()
NUM_PROJECT = CORPUS_MANAGER.num_project


#############################
# Tests
#############################
class TestProjectReader(unittest.TestCase):

    def setUp(self):
        self.reader = ProjectReader(PROJECT_ID, data_dir=DATA_DIR)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertIsNotNone(self.reader.project_id)

    def testListFiles(self):
        if IGNORE_TEST:
            return
        ffiles = self.reader.listFiles()
        self.assertGreater(len(ffiles), 0)

    def testGetFileAsStr(self):
        if IGNORE_TEST:
            return
        data = self.reader.getFileAsStr(PROJECT_FILE)
        self.assertGreater(len(data), 0)
        self.assertGreater(data.count("\n"), 10)

    def testGetCsvFileAsDf(self):
        if IGNORE_TEST:
            return
        df = self.reader.getCsvFileAsDf(PROJECT_FILE)
        self.assertGreater(len(df), 0)
        self.assertGreater(len(df.columns), 5)

    def testIterateProjects(self):
        if IGNORE_TEST:
            return
        def test(readers, expected_length):
            self.assertEqual(len(readers), expected_length)
            if len(readers) > 0:
                self.assertTrue(isinstance(readers[0], ProjectReader))
        #
        readers = [p for p in ProjectReader.iterateProjects(report_interval=NUM_PROJECT)]
        test(readers, NUM_PROJECT)
        #
        readers = [p for p in ProjectReader.iterateProjects(first=2, last=2)]
        test(readers, 1)
        #
        ignored_project_ids = CORPUS_MANAGER.project_ids
        readers = [p for p in 
                    ProjectReader.iterateProjects(ignored_project_ids=ignored_project_ids)]
        test(readers, 0)


if __name__ == '__main__':
    unittest.main()