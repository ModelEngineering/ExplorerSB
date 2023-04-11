"""Builds the index for search simulation abstracts"""

import src.ExplorerSB.constants as cn
from src.ExplorerSB.project import Project
from src.ExplorerSB import util

import os
import pandas as pd
from whoosh.index import create_in
from whoosh.fields import *
import pandas as pd

# Get the project context
if False:
    context_df = Project.buildContext(report_interval=1, sleep_sec=2.0)

# Get the output files
generator = Project.iterateProjects()
for project in generator:
    print("** Processing %s" % project.project_id)
    try:
        path = project._downloadOutput()
    except:
        print('*** Could not download project %s' % project.project_id)


if False:
    # Build the whoosh
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True),
        content=TEXT(stored=True))
    ix = create_in(cn.INDEX_DIR, schema)
    writer = ix.writer()

    # Iterate over project abstracts
    for project_id, row in context_df.iterrows():
        abstract = row[cn.ABSTRACT]
        citation = row[cn.CITATION]
        content = abstract + "   " + citation
        writer.add_document(title=project_id, path=u"/a", content=content)
    #
    writer.commit()