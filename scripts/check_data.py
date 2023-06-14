"""Checks the integrity of the data files the context file and their consistency with each other."""

from src.ExplorerSB import constants as cn
from src.ExplorerSB.project_reader import ProjectReader
from src.ExplorerSB.corpus_manager import CorpusManager

import os
import pandas as pd


CORPUS_MANAGER = CorpusManager()

#########
# Check the context file
#########
context_df = CORPUS_MANAGER.project_df 
# Report missing abstractions
missing_df = context_df[context_df[cn.ABSTRACT].isnull()]
blank_df = context_df[context_df[cn.ABSTRACT] == ""]
df = pd.concat([missing_df, blank_df])
if len(df) > 0:
    project_ids = df.index.tolist()
    print("\n\n***Missing abstracts for %d projects.\n%s" % (len(project_ids), str(project_ids)))
# Check that there is a zip file for each project
print("\n\n")
count_missing = 0
for reader in ProjectReader.iterateProjects(report_interval=CORPUS_MANAGER.num_project):
    if not os.path.exists(reader.getZipDirPath()):
        count_missing += 1
        print("***Missing zip file for %s" % reader.project_id)
print("\n***Missing zip files for %d projects" % count_missing)
