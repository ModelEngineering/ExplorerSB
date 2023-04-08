"""Builds the index for search simulation abstracts"""
import whoosh
from whoosh.index import create_in
from whoosh.fields import *
import pandas as pd

import src.ExplorerSB.constants as cn

API_URL = "https://api.biosimulations.org"
PROJECT_URL = "%s/projects" % API_URL
ABSTRACT_DF = pd.read_csv(cn.ABSTRACT_FILE)

# Initialize the indexer
schema = Schema(title=TEXT(stored=True), path=ID(stored=True),
      content=TEXT(stored=True))
ix = create_in(cn.INDEX_DIR, schema)
writer = ix.writer()

# Iterate over project abstracts
for idx, row in ABSTRACT_DF.iterrows():
    abstract = row[cn.ABSTRACT]
    citation = row[cn.CITATION]
    content = abstract + "   " + citation
    project_id = row[cn.PROJECT_ID]
    writer.add_document(title=project_id, path=u"/a", content=content)
#
writer.commit()
