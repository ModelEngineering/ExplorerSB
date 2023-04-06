"""Constructs the context for a project. Context is used ONLY to build information about projects."""

'''
TODO:
1. Don't use Project object since this will only use built information.
'''

import src.ExplorerSB.constants as cn
from src.ExplorerSB.searcher import Searcher
from src.ExplorerSB.summary_parser import SummaryParser

import os
import pandas as pd
import requests
import typing




class ProjectContext(object):
    # Use getProjectIds to initialize
    PROJECT_DCT = None
    PROJECT_IDS = None


    # FIXME: obtain runid
    def __init__(self, project_id: str):
        """
        Creates the context entry for a project.

        Args:
            project (Project)
        """
        self.project_id = project_id
        self.summary_parsers = None
        # Context
        self.project_id = project_id
        self.runid = None
        self.abstract = None
        self.citation = None
        self.title = None
        self.doi = None

    def do(self):
        """
        Constructs the context entry for a project

        Returns:
            dict: key, value for each context entry
        """
        summary_parser = SummaryParser(self.project_id)
        summary_parser.do()
        self.abstract = summary_parser.abstract
        self.citation = summary_parser.citation
        self.title = summary_parser.title
        self.doi = summary_parser.doi
        #
        self._copyFiles()
    
    @classmethod
    def getProjectIds(cls):
        """
        Initializes values of the project ids
        """
        response = requests.get(cn.PROJECT_URL)
        project_descs = response.json()
        _, response
        cls.PROJECT_DCT = {d["id"]: d for d in project_descs}
        cls.PROJECT_IDS = list(cls.PROJECT_DCT.keys())
        import pdb; pdb.set_trace()
