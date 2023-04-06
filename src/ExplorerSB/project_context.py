"""Constructs the context for a project. Context is used ONLY to build information about projects."""

'''
TODO:
1. Don't use Project object since this will only use built information.
'''

import src.ExplorerSB.constants as cn
from src.ExplorerSB.searcher import Searcher
from src.ExplorerSB.project import Project

from html.parser import HTMLParser
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
        self.project_id = project.project_id
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
        self.context_dct = {}
        self.summary_dct, self.summary_str = self._getSummaryDct()
        # Context created
        self.doi = self._extractDOI()
        self.abstract = self._getAbstract()
        self.citation = self._extractCitation()
        self.title = self._extractTitle()
        self._copyFiles()

    def _getSummaryDct(self)->typing.Tuple[typing.Dict, str]:
        """
        Gets the project summary as a nested dictionary.

        Returns
        -------
        dict: dictionary representation of the summary
        str: string representation of the summary
        """
        summary_url = "%s/projects/%s/summary" % (API_URL, self.project_id)
        response = requests.get(summary_url)
        summary_str = response.decomde()
        null = None
        return eval(response.content.decode()), summary_str
    
    @classmethod
    def getProjectIds(cls):
        """
        Initializes values of the project ids
        """
        response = requests.get(cn.PROJECT_URL)
        project_descs = response.json()
        cls.PROJECT_DCT = {d["id"]: d for d in project_descs}
        cls.PROJECT_IDS = list(PROJECT_DCT.keys())
