import src.ExplorerSB.util as util
import src.ExplorerSB.constants as cn

import os
import unittest


IGNORE_TEST = True
IS_PLOT = False


#############################
# Tests
#############################
class TestFunctions(unittest.TestCase):

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

    def testReadBiosimulations(self):
        if IGNORE_TEST:
            return
        url1 = "https://api.biosimulations.org/projects"
        response, response_str, response_nst = util.readBiosimulations(url1)
        self.assertTrue(isinstance(response_str, str))
        self.assertTrue("Response" in str(type(response)))
        self.assertTrue(isinstance(response_nst, list))
        self.assertTrue(isinstance(response_nst[0], dict))

    def testGetBiomodelInfo(self):
        #if IGNORE_TEST:
        #    return
        biomodel_id = "BIOMD0000000297"
        response_dct = util.getBiomodelInfo(biomodel_id)
        self.assertTrue(isinstance(response_dct, dict))
        trues = [k in response_dct.keys() for k in ['title', 'synopsis', 'year', 'link', 'authors']]
        self.assertTrue(all(trues))
        import pdb; pdb.set_trace()




if __name__ == '__main__':
  unittest.main()