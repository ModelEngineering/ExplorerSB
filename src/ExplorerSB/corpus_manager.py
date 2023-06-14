'''Creates python data structures from previously built context.csv and data/*.zip directories.'''

"""
Conventions:
    In general, the key for a dictionary is the project_id.
    Dictionaries with an "inv" prefix, have a value of project_id.
"""


import src.ExplorerSB.constants as cn

import os
import pandas as pd


class CorpusManager(object):

    def __init__(self, data_dir=cn.DATA_DIR, tmp_dir=cn.TMP_DIR):
        """
        Creates convenient python data structures for the corpus of projects.

        Args:
            data_dir: str (path to context.csv, zip files)
        """
        self.data_dir = data_dir
        self.context_path = os.path.join(self.data_dir, cn.CONTEXT_FILE_NAME) + ".csv"
        self.project_df = pd.read_csv(self.context_path)
        self.num_project = len(self.project_df)
        self.project_df = self.project_df.drop_duplicates()
        self.project_df = self.project_df.set_index(cn.PROJECT_ID)
        self.project_ids = self.project_df.index.to_list()
        self.tmp_dir = tmp_dir
        if not os.path.isdir(self.tmp_dir):
            os.mkdir(self.tmp_dir)