import src.ExplorerSB.constants as cn
import src.ExplorerSB.project as pjt

import os
import pandas as pd
import shutil
import unittest
import urllib3


IGNORE_TEST = False
IS_PLOT = False
PROJECT_ID = "iYS854"
PROJECT_ID = "Yeast-cell-cycle-Irons-J-Theor-Biol-2009"
TEMP_DIR = os.path.dirname(os.path.abspath(__file__))
CONTEXT_FILE = os.path.join(TEMP_DIR, "context.csv")
SAVED_CONTEXT_FILE = os.path.join(TEMP_DIR, "saved_context.csv")
if not os.path.isfile(SAVED_CONTEXT_FILE):
    _ = pjt.Project.buildContext(out_path=SAVED_CONTEXT_FILE, first=0, last=2)


#############################
# Tests
#############################
class TestProject(unittest.TestCase):

    def setUp(self):
        if IGNORE_TEST:
           return
        self.project = self.getInitializedProject()

    def mkdir(self, project):
        dir_path = os.path.join(TEMP_DIR, project.runid)
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        return dir_path

    def rmdir(self, dir_path):
        shutil.rmtree(dir_path)

    def getInitializedProject(self, project_id=PROJECT_ID):
        if "project" in dir(self):
            project = self.project
        else:
            project = pjt.Project(project_id)
            project.initializeClass()
            project.runid = project._getRunid()
        return project

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertIsNotNone(self.project.project_id)

    def testInitializeClass(self):
        if IGNORE_TEST:
            return
        project = pjt.Project(PROJECT_ID)
        project.initializeClass()
        self.assertIsNotNone(project.PROJECT_DCT)

    def testCopyUrlFile(self):
        if IGNORE_TEST:
            return
        project = self.getInitializedProject()
        dir_path = self.mkdir(project)
        def test(url):
            file_path = project._copyUrlFile(url, dir_path=TEMP_DIR)
            self.assertTrue(os.path.isfile(file_path))
        #
        urls = [
                "https://storage.googleapis.com/files.biosimulations.org/simulations/621d90b9b50991044c7a1ea6/contents/iYS854.xml",
                "https://storage.googleapis.com/files.biosimulations.org/simulations/621d42c187550e369891bbdb/contents/screenshot4.png"
        ]
        for url in urls:
            test(url)
        self.rmdir(dir_path)
    
    def testGetUrlFileList(self):
        if IGNORE_TEST:
           return
        project = self.getInitializedProject()
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
        project = self.getInitializedProject()
        dir_path = self.mkdir(project)
        ffiles = project._copyUrlFiles(dir_path=dir_path)
        for ffile in ffiles:
            self.assertTrue(os.path.isfile(ffile))
        self.rmdir(dir_path)

    def testBuildProject(self):
        if IGNORE_TEST:
            return
        self.project.buildProject()
        for attribute in cn.CONTEXT_KEYS:
            self.assertIsNotNone(self.project.__getattribute__(attribute))
        self.assertGreater(len(self.project.abstract), 0)
    
    def testBuildContext(self):
        if IGNORE_TEST:
            return
        if os.path.isfile(CONTEXT_FILE):
            os.remove(CONTEXT_FILE)
        df = pjt.Project.buildContext(out_path=CONTEXT_FILE, report_interval=1, first=0, last=2)
        self.assertTrue(os.path.isfile(CONTEXT_FILE))
        os.remove(CONTEXT_FILE)

    def testInitialize(self):
        if IGNORE_TEST:
            return
        pjt.Project.PROJECT_DF = None
        self.project.initialize()
        for key in cn.CONTEXT_KEYS:
            self.assertIsNotNone(self.project.__getattribute__(key))
    
    def testGetFilePaths(self):
        if IGNORE_TEST:
            return
        ffiles = self.project.getFilePaths()
        self.assertGreater(len(ffiles), 0)
        self.assertTrue(isinstance(ffiles[0], str))
        for ffile in ffiles:
            self.assertTrue(os.path.isfile(ffile))
    
    def testBuildContextBug(self):
        if IGNORE_TEST:
            return
        return
        if os.path.isfile(CONTEXT_FILE):
            os.remove(CONTEXT_FILE)
        df = pjt.Project.buildContext(out_path=CONTEXT_FILE, report_interval=1, first=19, last=None)
        self.assertTrue(os.path.isfile(CONTEXT_FILE))
        import pdb; pdb.set_trace()
        os.remove(CONTEXT_FILE)

    def testMakeReadableModel(self):
        if IGNORE_TEST:
            return
        project = self.getInitializedProject()
        model_str = project.makeReadableModel(is_write=True)
        cache_path = project.getCacheDirectory()
        # Initial tests
        self.assertIsNotNone(model_str)
        self.assertGreater(len(model_str), 0)
        # See if the file was written
        ffiles = os.listdir(cache_path)
        is_good = any([f for f in ffiles if ".ant" in f])
        self.assertTrue(is_good)
    
    def testIterateProjects(self):
        if IGNORE_TEST:
            return
        projects = [p for p in pjt.Project.iterateProjects()]
        self.assertGreater(len(projects), 0)
        self.assertTrue(isinstance(projects[0], pjt.Project))
    
    def testDownloadOutput(self):
        if IGNORE_TEST:
            return
        project = self.getInitializedProject()
        path = project._downloadOutput()
        self.assertTrue(os.path.isdir(path))
        ffiles = os.listdir(path)
        self.assertGreater(len(ffiles), 0)

    def testGetH5FilePath(self):
        if IGNORE_TEST:
            return
        project = self.getInitializedProject()
        path = project.getH5FilePath()
        self.assertTrue(os.path.isfile(path))
        splits = os.path.splitext(path)
        self.assertEqual(splits[1], ".h5")

    def testGetH5Data(self):
        if IGNORE_TEST:
            return
        project = self.getInitializedProject()
        dfs = project.getH5Data()
        self.assertGreater(len(dfs), 0)
        self.assertTrue(isinstance(dfs[0], pd.DataFrame))
        path = project.getCacheDirectory()
        csv_files = [p for p in os.listdir(path) if ".csv" in p]
        self.assertEqual(len(dfs), len(csv_files))


if __name__ == '__main__':
    unittest.main()