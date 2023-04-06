import src.ExplorerSB.util as util
import src.ExplorerSB.constants as cn

import os
import unittest


IGNORE_TEST = False
IS_PLOT = False
TEMP_DIR = os.path.join(cn.TEST_DIR, "temp")



#############################
# Tests
#############################
class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.remove()

    def tearDown(self):
        self.remove()

    def remove(self):
        ffiles = os.listdir(TEMP_DIR)
        for ffile in ffiles:
            if ffile[0:2] != "__":
                path = os.path.join(TEMP_DIR, ffile)
                os.remove(path)

    def testIndexNested(self):
        if IGNORE_TEST:
            return
        struct = [dict(a=[1, 2, 3], b=4), 3]
        #
        result = util.indexNested(struct, [0, "b"])
        self.assertEqual(result, 4)
        #
        result = util.indexNested(struct, [0, "a", 0])
        self.assertEqual(result, 1)
        #
        result = util.indexNested(struct, ["a", 0])
        self.assertIsNone(result)

    def testRemoveAngleBrackets(self):
        if IGNORE_TEST:
            return
        text = "hello <b class=x other=y>this is text</b> goodby"
        new_text = util.removeAngleBrackets(text)
        self.assertEqual(new_text, "hello this is text")

    def testGetApikey(self):
        if IGNORE_TEST:
            return
        apikey = util.getApikey()
        self.assertTrue(isinstance(apikey, str))
        self.assertGreater(len(apikey), 20)

    def testReadFileFromURL(self):
        if IGNORE_TEST:
            return
        url = "https://storage.googleapis.com/files.biosimulations.org/simulations/621d90b9b50991044c7a1ea6/contents/iYS854.xml"
        util.copyUrlFile(url, TEMP_DIR)
        path = os.path.join(TEMP_DIR, util.getFilenameFromUrl(url))
        self.assertTrue(os.path.isfile(path))

    def testReadBiosimulations(self):
        if IGNORE_TEST:
            return
        url1 = "https://api.biosimulations.org/projects"
        response, response_str = util.readBiosimulations(url1)
        self.assertTrue(isinstance(response_str, str))
        self.assertTrue("Response" in str(type(response)))




if __name__ == '__main__':
  unittest.main()
