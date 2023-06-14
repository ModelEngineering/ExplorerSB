"""Builds the index for search simulation abstracts"""

'''
The build is done in sections so that builds can be done selectively.
'''

import src.ExplorerSB.constants as cn
from src.ExplorerSB.project_reader import Project
from src.ExplorerSB import util
from src.ExplorerSB.json_converter import convertCSVToJSON

import os
import pandas as pd
from whoosh.index import create_in
from whoosh.fields import *
import pandas as pd
import zipfile

# Construct the project contex
context_df = Project.buildContext(report_interval=1, sleep_sec=2.0)
convertCSVToJSON(cn.CONTEXT_FILE, cn.CONTEXT_JSON_FILE)

# Download the output files
if True:
    generator = Project.iterateProjects()
    for project in generator:
        print("** Processing %s" % project.project_id)
        try:
            path = project._downloadOutput()
        except:
            print('*** Could not download project %s' % project.project_id)

# Create CSV files for h5 files
if True:
    generator = Project.iterateProjects()
    for project in generator:
        print("** Creating CSV files for %s" % project.project_id)
        path = project.getH5FilePath()
        if path is not None:
            _ = project.getH5Data()

# Get the omex files and unzip them
if True:
    generator = Project.iterateProjects(report_interval=1, first=0)
    url_pat = "https://api.biosimulations.org/runs/%s/download"
    for project in generator:
        url = url_pat % project.runid
        cache_path = project.getCacheDirectory()
        project._copyUrlFile(url, cache_path)
        file_path = os.path.join(cache_path, "download")
        new_file_path = os.path.join(cache_path, "download.zip")
        os.rename(file_path, new_file_path)
        with zipfile.ZipFile(new_file_path, 'r') as zip_ref:
            zip_ref.extractall(cache_path)

# Build readable model files (part of buildContext)
if True:
    generator = Project.iterateProjects(report_interval=1, first=71)
    for project in generator:
        project.makeReadableModel(is_replace=True)

# Construct the whoosh schema
if True:
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