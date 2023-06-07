import src.ExplorerSB.constants as cn
from src.ExplorerSB.h5converter import H5Converter 

import os
import unittest


IGNORE_TEST = True
IS_PLOT = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
H5_PATH = os.path.join(TEST_DIR, "test_reports.h5")
CSV_DIR = os.path.join(TEST_DIR, "test_csv_files")
DATASET_NAMES = ['autogen_report_for_task1', 'autogen_plot_for_task1']
DATASET_FILE = "%s.csv" % DATASET_NAMES[1]


#############################
# Tests
#############################
class TestProjectBuilder(unittest.TestCase):

    def setUp(self):
        self.converter = H5Converter(H5_PATH, csv_dir=CSV_DIR)
        self.remove()

    def tearDown(self):
        self.remove()
    
    def remove(self):
        ffiles = os.listdir(CSV_DIR)
        for ffile in ffiles:
            path = os.path.join(CSV_DIR, ffile)
            if os.path.isfile(path):
                os.remove(path)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertIsNotNone(self.converter.h5_path)

    def testMakeDescriptorDct(self):
        if IGNORE_TEST:
            return
        self.converter._makeDescriptorDct()
        self.assertTrue(len(self.converter.descriptor_dct) > 0)
        trues = [n in self.converter.descriptor_dct.keys() for n in DATASET_NAMES]
        self.assertTrue(all(trues))
        trues = [len(self.converter.descriptor_dct[k].df) > 0 for k in self.converter.descriptor_dct.keys()]
        self.assertTrue(all(trues))

    def testRenamePlotColumns(self):
        if IGNORE_TEST:
            return
        self.converter._makeDescriptorDct()
        self.converter._renamePlotColumns()
        # FIXME: check the column names for _
        for descriptor in self.converter.descriptor_dct.values():
            if "plot" in descriptor.name:
                trues = [not "_" in l for l in descriptor.df.columns]
                self.assertTrue(all(trues))

    def testCreateResult(self):
        if IGNORE_TEST:
            return
        self.converter._makeDescriptorDct()
        self.converter._renamePlotColumns()
        self.converter._createResult()
        self.assertTrue(len(self.converter.result_dct) > 0)
        trues = [n in DATASET_NAMES for n in self.converter.result_dct.keys()]
        self.assertTrue(all(trues))
        trues = [len(self.converter.result_dct[k]) > 0 for k in self.converter.result_dct.keys()]
        self.assertTrue(all(trues))

    def testWriteCsv(self):
        #if IGNORE_TEST:
        #    return
        self.converter._makeDescriptorDct()
        self.converter._renamePlotColumns()
        self.converter._createResult()
        self.converter._writeCsv()
        true = DATASET_FILE in os.listdir(CSV_DIR)
        self.assertTrue(true)


if __name__ == '__main__':
    unittest.main()