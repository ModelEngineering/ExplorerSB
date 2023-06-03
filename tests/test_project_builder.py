import src.ExplorerSB.constants as cn
from src.ExplorerSB.project_builder import ProjectBuilder

import os
import pandas as pd
import shutil
import unittest
import urllib3


IGNORE_TEST = True
IS_PLOT = False
PROJECT_ID = "Yeast-cell-cycle-Irons-J-Theor-Biol-2009"
RUNID = "61fea483f499ccf25faafc4d"
PROJECT_ID = "BIOMD0000000001_amici_A_kinetic_mechanism_for_nicoti"
RUNID = "647106f00dcacb55678b35f4"
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(TEST_DIR, "test_data")
STAGE_DIR = os.path.join(TEST_DIR, "stage_data")
CONTEXT_FILE = os.path.join(DATA_DIR, "context.csv")
SAVED_CONTEXT_FILE = os.path.join(DATA_DIR, "saved_context.csv")
URLS = [
                "https://storage.googleapis.com/files.biosimulations.org/simulations/621d90b9b50991044c7a1ea6/contents/iYS854.xml",
                "https://storage.googleapis.com/files.biosimulations.org/simulations/621d42c187550e369891bbdb/contents/screenshot4.png"
        ]


#############################
# Tests
#############################
class TestProjectBuilder(unittest.TestCase):

    def setUp(self):
        self.builder = self.makeBuilder()

    def mkdir(self, project):
        dir_path = os.path.join(project.data_dir, project.runid)
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        return dir_path

    def rmdir(self, dir_path):
        shutil.rmtree(dir_path)

    def makeBuilder(self, project_id=PROJECT_ID, runid=RUNID):
        builder = ProjectBuilder(project_id, runid, data_dir=DATA_DIR, stage_dir=STAGE_DIR)
        # Ensure that the project cache is present
        _ = builder.getProjectDir(STAGE_DIR, is_create=True)
        return builder

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertIsNotNone(self.builder.project_id)
        stage_dir = self.builder.getProjectDir(STAGE_DIR)
        self.assertTrue(os.path.isdir(stage_dir))

    def testGetUrlFileList(self):
        if IGNORE_TEST:
           return
        builder = self.makeBuilder()
        urls = builder._getUrlFileList()
        for url in urls:
            try:
                _ = urllib3.util.parse_url(url)
                is_parsed = True
            except:
                is_parsed = False
            self.assertTrue(is_parsed)

    def testCopyUrlFile(self):
        if IGNORE_TEST:
            return
        project = self.makeBuilder()
        dir_path = self.mkdir(project)
        def test(url):
            file_path = project._copyUrlFile(url, dir_path)
            self.assertTrue(os.path.isfile(file_path))
        #
        ffiles = os.listdir(dir_path)
        self.assertEqual(len(ffiles), 0)
        for url in URLS:
            test(url)
        ffiles = os.listdir(dir_path)
        self.assertGreater(len(ffiles), 0)
        self.rmdir(dir_path)

    def testGetFilePaths(self):
        #if IGNORE_TEST:
        #    return
        # Setup
        url = URLS[0]
        _ = self.mkdir(self.builder)
        dest_dir = self.builder.getProjectDir(self.builder.stage_dir)
        file_path = self.builder._copyUrlFile(url, dest_dir)
        # Test
        ffiles = self.builder.getFilePaths(dest_dir=self.builder.stage_dir)
        self.assertGreater(len(ffiles), 0)
        self.assertTrue(isinstance(ffiles[0], str))
        for ffile in ffiles:
            self.assertTrue(os.path.isfile(ffile))
        self.rmdir(dest_dir) 

    # TESTME 
    def testDownloadOutput(self):
        if IGNORE_TEST:
            return
        builder = self.makeBuilder()
        path = builder._downloadOutput()
        self.assertTrue(os.path.isdir(path))
        ffiles = os.listdir(path)
        self.assertGreater(len(ffiles), 0)

    def testGetH5FilePath(self):
        if IGNORE_TEST:
            return
        builder = self.makeBuilder()
        path = builder._getH5FilePath()
        self.assertTrue(os.path.isfile(path))
        splits = os.path.splitext(path)
        self.assertEqual(splits[1], ".h5")

    def testGetH5Data(self):
        if IGNORE_TEST:
            return
        builder = self.makeBuilder()
        dfs = builder._makeCSVFiles()
        self.assertGreater(len(dfs), 0)
        self.assertTrue(isinstance(dfs[0], pd.DataFrame))
        path = builder.getProjectDir()
        csv_files = [p for p in os.listdir(path) if ".csv" in p]
        self.assertEqual(len(dfs), len(csv_files))

    def testBuildProject(self):
        if IGNORE_TEST:
            return
        self.builder.buildProject()
        for attribute in cn.CONTEXT_KEYS:
            self.assertIsNotNone(self.builder.__getattribute__(attribute))
        self.assertGreater(len(self.builder.abstract), 0)
        # Check the files
        paths = self.builder.getFilePaths()
        for path in paths:
            self.assertTrue(os.path.isfile(path))
    
    def testBuildContext(self):
        if IGNORE_TEST:
            return
        if os.path.isfile(CONTEXT_FILE):
            os.remove(CONTEXT_FILE)
        _ = ProjectBuilder.buildContext(context_file_path=CONTEXT_FILE, report_interval=1, first=0, last=2, data_dir=DATA_DIR)
        self.assertTrue(os.path.isfile(CONTEXT_FILE))
        with open(CONTEXT_FILE, "r") as fd:
            lines = fd.readlines()
        self.assertGreater(len(lines), 2)
        os.remove(CONTEXT_FILE)

    def testMakeReadableModel(self):
        if IGNORE_TEST:
            return
        builder = self.makeBuilder()
        _ = builder._makeStagingData() 
        model_str = builder._makeReadableModel(is_write=True)
        cache_path = builder.getProjectDir()
        # Initial tests
        self.assertIsNotNone(model_str)
        self.assertGreater(len(model_str), 0)
        # See if the file was written
        ffiles = os.listdir(cache_path)
        is_good = any([f for f in ffiles if ".ant" in f])
        self.assertTrue(is_good)
   

if __name__ == '__main__':
    unittest.main()