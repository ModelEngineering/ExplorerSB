"""
Builds the context needed to run ExploerSB.
1. Files for projects are placed in cn.CACHE_DIR
2. Builds context.csv (project_id, citation, abstract, runid, title)
Then, builds the index for whoosh in local/indexdir
"""

import src.ExplorerSB.constants as cn
from src.ExplorerSB.searcher import Searcher
from src.ExplorerSB.project import Project

from html.parser import HTMLParser
import os
import pandas as pd
import requests
import typing

def main():
    """
    Iterates across all projects to build context.
    """ 
    project_ids = Project.getProjectIds()
    for project_id in project_ids:
        project = Project(project_id)
    