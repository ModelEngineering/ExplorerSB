'''Encapsulates all information about a previously built project'''

'''
TO DO:
1. Should just use "built" information, the file context.csv and the contents of CACHE_DIR.
'''


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util
from src.ExplorerSB.searcher import Searcher

from dash import html
from htmldom import htmldom
from requests_html import HTMLSession
import numpy as np
import json
import os
import pandas as pd
import requests
import yaml



######## Constants #######
ABSTRACT_DF = pd.read_csv(cn.ABSTRACT_FILE)
ABSTRACT_DF.index = ABSTRACT_DF[cn.ID]
ABSTRACT_DF = util.cleanDF(ABSTRACT_DF)



class Project(object):
    project_ids = None

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
        self.summary_dct = self._getSummaryDct()
        self.runid = util.indexNested(self.summary_dct, ["simulationRun", "id"])

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
    def cacheFiles(self):
        """
        Writes the files for this runid to the cache.

        Returns
        -------
        list-str (each string is a URL)
        """
        url = API_URL + "/files/" + self.runid
        response = requests.get(url)
        null = None
        false = False
        true = True
        lst = eval(response.content.decode())
        urls = [x["url"] for x in lst]
        # Write the files to cache
        dir_path = os.path.join(cn.CACHE_DIR, self.runid)
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        for url in urls:
            util.copyUrlFile(url, dir_path)
        #
        return urls
    
    def listFiles(self)->list[str]:
        """
        Lists al files for the project

        Returns:
            list[str]: list of file paths
        """
        path_dir = os.path.join(cn.CACHE_DIR, self.runid)
        return os.listdir(path_dir)

    
