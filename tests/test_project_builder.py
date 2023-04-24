import src.ExplorerSB.constants as cn
from src.ExplorerSB.project_builder import ProjectBuilder

import os
import pandas as pd
import shutil
import unittest
import urllib3


IGNORE_TEST = False
IS_PLOT = False
PROJECT_ID = "Yeast-cell-cycle-Irons-J-Theor-Biol-2009"
PROJECT_RUNID = "61fea483f499ccf25faafc4d"
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DATA_DIR, "test_data")
CONTEXT_FILE = os.path.join(DATA_DIR, "context.csv")
SAVED_CONTEXT_FILE = os.path.join(DATA_DIR, "saved_context.csv")


#############################
# Tests
#############################
class TestProjectBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_dir = DATA_DIR
        if os.path.isdir(cls.data_dir):
            shutil.rmtree(cls.data_dir)
        os.mkdir(cls.data_dir)
        project_cache_dir = os.path.join(cls.data_dir, PROJECT_RUNID)
        os.mkdir(project_cache_dir)
        #
        if not os.path.isfile(SAVED_CONTEXT_FILE):
            _ = ProjectBuilder.buildContext(context_file_path=SAVED_CONTEXT_FILE, data_dir=DATA_DIR, first=0, last=2)
        #
        return super().setUpClass() 
    
    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(cls.data_dir):
            shutil.rmtree(cls.data_dir)
        return super().tearDownClass() 

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

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertIsNotNone(self.builder.project_id)

    def makeBuilder(self, project_id=PROJECT_ID):
        builder = ProjectBuilder(project_id, data_dir=DATA_DIR)
        builder.initializeClass()
        builder.runid = builder._getRunid()
        # Ensure that the project cache is present
        _ = builder.getProjectCacheDirectory(is_create=True)
        return builder

    def testInitializeClass(self):
        if IGNORE_TEST:
            return
        project = ProjectBuilder(PROJECT_ID)
        project.initializeClass()
        self.assertIsNotNone(project.PROJECT_DCT)

    def testCopyUrlFile(self):
        if IGNORE_TEST:
            return
        project = self.makeBuilder()
        dir_path = self.mkdir(project)
        def test(url):
            file_path = project._copyUrlFile(url, dir_path)
            self.assertTrue(os.path.isfile(file_path))
        #
        urls = [
                "https://storage.googleapis.com/files.biosimulations.org/simulations/621d90b9b50991044c7a1ea6/contents/iYS854.xml",
                "https://storage.googleapis.com/files.biosimulations.org/simulations/621d42c187550e369891bbdb/contents/screenshot4.png"
        ]
        ffiles = os.listdir(dir_path)
        self.assertEqual(len(ffiles), 0)
        for url in urls:
            test(url)
        ffiles = os.listdir(dir_path)
        self.assertGreater(len(ffiles), 0)
        self.rmdir(dir_path)
    
    def testGetUrlFileList(self):
        if IGNORE_TEST:
           return
        project = self.makeBuilder()
        urls = project._getUrlFileList()
        for url in urls:
            try:
                _ = urllib3.util.parse_url(url)
                is_parsed = True
            except:
                is_parsed = False
            self.assertTrue(is_parsed)

    def testCopyUrlFiles(self):
        if IGNORE_TEST:
           return
        builder = self.makeBuilder()
        project_cache_dir = self.mkdir(builder)
        ffiles = builder._copyUrlFiles()
        for ffile in ffiles:
            self.assertTrue(os.path.isfile(ffile))
        self.rmdir(project_cache_dir)

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
    
    def testGetFilePaths(self):
        if IGNORE_TEST:
            return
        ffiles = self.builder.getFilePaths()
        self.assertGreater(len(ffiles), 0)
        self.assertTrue(isinstance(ffiles[0], str))
        for ffile in ffiles:
            self.assertTrue(os.path.isfile(ffile))

    def testMakeReadableModel(self):
        #if IGNORE_TEST:
        #    return
        builder = self.makeBuilder()
        _ = builder._copyUrlFiles() 
        model_str = builder.makeReadableModel(is_write=True)
        cache_path = builder.getProjectCacheDirectory()
        # Initial tests
        self.assertIsNotNone(model_str)
        self.assertGreater(len(model_str), 0)
        # See if the file was written
        ffiles = os.listdir(cache_path)
        is_good = any([f for f in ffiles if ".ant" in f])
        self.assertTrue(is_good)
    
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
        path = builder.getH5FilePath()
        self.assertTrue(os.path.isfile(path))
        splits = os.path.splitext(path)
        self.assertEqual(splits[1], ".h5")

    def testGetH5Data(self):
        if IGNORE_TEST:
            return
        builder = self.makeBuilder()
        dfs = builder.getH5Data()
        self.assertGreater(len(dfs), 0)
        self.assertTrue(isinstance(dfs[0], pd.DataFrame))
        path = builder.getProjectCacheDirectory()
        csv_files = [p for p in os.listdir(path) if ".csv" in p]
        self.assertEqual(len(dfs), len(csv_files))


if __name__ == '__main__':
    unittest.main()