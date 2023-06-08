import src.ExplorerSB.constants as cn
from src.ExplorerSB.builder import Builder

import os
import pandas as pd
import shutil
import unittest


IGNORE_TEST = False
IS_PLOT = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PROJECTS_CSV = os.path.join(TEST_DIR, "test_projects.csv")
DATA_DIR = os.path.join(TEST_DIR, "test_data")
STAGE_DIR = os.path.join(TEST_DIR, "stage_data")
CSV_CONTEXT_FILE = os.path.join(DATA_DIR, "context.csv")
JSON_CONTEXT_FILE = os.path.join(DATA_DIR, "context.json")
REMOVE_FILES = [CSV_CONTEXT_FILE, JSON_CONTEXT_FILE]

############################
# Tests
#############################
class TestBuilder(unittest.TestCase):

    def setUp(self):
        self.builder =  Builder(project_specification_csv=TEST_PROJECTS_CSV,
                                stage_dir=STAGE_DIR, 
                                data_dir=DATA_DIR, 
                                )
        self.remove_subdirectories()
    
    def tearDown(self):
        self.remove_subdirectories()

    def remove_subdirectories(self):
        def remove_subdirectories(dir_path):
            directories = os.listdir(dir_path)
            for path in directories:
                full_path = os.path.join(dir_path, path)
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
        #
        remove_subdirectories(self.builder.data_dir)
        remove_subdirectories(self.builder.stage_dir)
        #
        for ffile in REMOVE_FILES:
            if os.path.isfile(ffile):
                os.remove(ffile)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertTrue(os.path.isfile(TEST_PROJECTS_CSV))
        self.assertTrue(os.path.isdir(DATA_DIR))
        self.assertTrue(os.path.isdir(STAGE_DIR))
        self.assertEqual(self.builder.project_specification_csv, TEST_PROJECTS_CSV)

    def testInitialize(self):
        if IGNORE_TEST:
            return
        self.builder._initialize()
        self.assertGreater(len(self.builder.project_ids), 0)
        self.assertGreater(len(self.builder.runid_dct), 0)

    def testBuild(self):
        if IGNORE_TEST:
            return
        self.builder.build()
        self.assertTrue(os.path.isfile(CSV_CONTEXT_FILE))
        self.assertTrue(os.path.isfile(JSON_CONTEXT_FILE))
        df = pd.read_csv(CSV_CONTEXT_FILE)
        self.assertGreater(len(df), 0)
        trues = [c in df.columns for c in cn.CONTEXT_KEYS]
        self.assertTrue(all(trues))


if __name__ == '__main__':
    unittest.main()