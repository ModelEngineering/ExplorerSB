import src.ExplorerSB.constants as cn
import src.ExplorerSB.project as pjt

import os
import shutil
import unittest
import urllib3


IGNORE_TEST = True
IS_PLOT = False
PROJECT_ID = "iYS854"
PROJECT_ID = "Yeast-cell-cycle-Irons-J-Theor-Biol-2009"
TEMP_DIR = os.path.dirname(os.path.abspath(__file__))
CONTEXT_FILE = os.path.join(TEMP_DIR, "context.csv")


#############################
# Tests
#############################
class TestProject(unittest.TestCase):

    def setUp(self):
        self.project = self.getInitializedProject()

    def mkdir(self, project):
        dir_path = os.path.join(TEMP_DIR, project.runid)
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        return dir_path

    def rmdir(self, dir_path):
        shutil.rmtree(dir_path)

    def getInitializedProject(self):
        project = pjt.Project(PROJECT_ID)
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
        project = pjt.Project(PROJECT_ID, is_usecontext=False)
        project.initializeClass()
        self.assertIsNotNone(project.PROJECT_DCT)

    def testGetFilePaths(self):
        if IGNORE_TEST:
            return
        ffiles = self.project.getFilePaths()
        self.assertGreater(len(ffiles), 0)
        self.assertTrue(isinstance(ffiles[0], str))
        for ffile in ffiles:
            if not os.path.isfile(ffile):
                print(ffile)
            self.assertTrue(os.path.isfile(ffile))

    def testCopyUrlFile(self):
        if IGNORE_TEST:
            return
        project = self.getInitializedProject()
        dir_path = self.mkdir(project)
        file_url = "https://storage.googleapis.com/files.biosimulations.org/simulations/621d90b9b50991044c7a1ea6/contents/iYS854.xml"
        file_path = project._copyUrlFile(file_url, dir_path=TEMP_DIR)
        self.assertTrue(os.path.isfile(file_path))
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
        import pdb; pdb.set_trace()
        for attribute in cn.CONTEXT_KEYS:
            self.assertIsNotNone(self.project.__getattribute__(attribute))
    
    def testBuildContext(self):
        #if IGNORE_TEST:
        #    returna
        df = pjt.Project.buildContext(out_path=CONTEXT_FILE, report_interval=1, first=0, last=5)
        import pdb; pdb.set_trace()


if __name__ == '__main__':
  unittest.main()