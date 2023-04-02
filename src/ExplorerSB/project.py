'''Collects information for a simulation project'''


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util
from src.ExplorerSB.searcher import Searcher

from dash import html
import numpy as np
import json
import pandas as pd
import requests
import yaml
from htmldom import htmldom
from requests_html import HTMLSession


######## Constants #######
ABSTRACT_DF = pd.read_csv(cn.ABSTRACT_FILE)
ABSTRACT_DF.index = ABSTRACT_DF[cn.ID]
ABSTRACT_DF = util.cleanDF(ABSTRACT_DF)
API_URL = "https://api.biosimulations.org"
PROJECT_URL = "%s/projects" % API_URL
response = requests.get(PROJECT_URL)
project_descs = response.json()
PROJECT_DCT = {d["id"]: d for d in project_descs}
PROJECT_IDS = list(PROJECT_DCT.keys())
# The value is the abstract
PROJECT_DCT = {n: n if not n in ABSTRACT_DF.index
      else ABSTRACT_DF.loc[n, cn.TITLE] for n in PROJECT_IDS}


class Project(object):

    def __init__(self, project_id):
        """
        Parameters
        ----------
        project_id: str
        """
        self.project_id = project_id
        self.desc = PROJECT_DCT[self.project_id]
        self.abstract = ABSTRACT_DF.loc[project_id, cn.ABSTRACT]
        self.citation = ABSTRACT_DF.loc[project_id, cn.CITATION]
        self.title = ABSTRACT_DF.loc[project_id, cn.TITLE]
        self._file_urls = None
        self.summary_dct = self._getSummaryDct()
        self.simulation_run = util.indexNested(self.summary_dct,
              ["simulationRun", "id"])

    def _getSummaryDct(self):
        """
        Gets the project summary as a nested dictionary.

        Returns
        -------
        dict
        """
        summary_url = "%s/projects/%s/summary" % (API_URL, self.project_id)
        response = requests.get(summary_url)
        null = None
        return eval(response.content.decode())

    def getAbstractWithHighlights(self, search_result):
        """
        Creates Markdown text that bolds the highlights from search results.

        Parameters
        ----------
        search_result: whoosh.search

        Returns
        -------
        str (Markdown)
        """
        if search_result is not None:
            highlights = search_result.highlights("content")
            highlights = util.removeAngleBrackets(highlights)
            splits = highlights.split("...")
            for split in splits:
                bold_split = "**" + split + "**"
                abstract = self.abstract.replace(split, bold_split)
            return abstract
        else:
            return self.abstract

    # TODO: Finish
    def getFileUrls(self):
        """
        Extracts the URLs of files for the simulation run.

        Returns
        -------
        list-str (each string is a URL)
        """
        if self._file_urls is None:
            pass
        return self._file_urls
