"""Generates content for search and searches content"""


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util

import openai
import os
import pandas as pd
from whoosh.fields import *
from whoosh.qparser import QueryParser
import whoosh.index as index


# Refresh the key at https://platform.openai.com/account/api-keys
APIKEY = util.getApikey()
MODEL_ENGINE = "gpt-3.5-turbo"
if os.path.isfile(cn.ABSTRACT_FILE):
    ABSTRACT_DF = pd.read_csv(cn.ABSTRACT_FILE)
    ABSTRACT_DF.index = ABSTRACT_DF[cn.ID]
    ABSTRACT_DF = util.cleanDF(ABSTRACT_DF)
    ABSTRACTS = [v for v in ABSTRACT_DF.index]
else:
    ABSTRACT_DF = None


class Searcher(object):

    def __init__(self, api_key=APIKEY):
        self.api_key = api_key
        openai.api_key = self.api_key

    def get(self, citation_str):
        """
        Returns a summary of the article based on its citation.

        Parameters
        ----------
        citation_str: str

        Returns
        -------
        str
        """
        query_str = "Summarize the paper %s" % citation_str
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system",
                      "content": "You are a helpful assistant."},
                {"role": "user", "content": query_str},
            ])
        return response.choices[0]['message']["content"]

    def search(self, query_str, index_dir=cn.INDEX_DIR):
        """
        Searches the index for the terms. Searching includes
            OR, AND, ~<n> (number of replacement terms)

        Parameters
        ----------
        query_str: str
        index_dir: str (path to index directory)

        Returns
        -------
        list-str (list of project ids), list-results
        """
        if ABSTRACT_DF is None:
            raise ValueError("Must build %s before doing search" % cn.ABSTRACT_FILE)
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True),
              content=TEXT(stored=True))
        indexer = index.open_dir(index_dir)
        this_searcher = indexer.searcher()
        parser = QueryParser("content", indexer.schema)
        #parser.add_plugin(qparser.FuzzyTermPlugin())
        query = parser.parse(query_str)
        results = this_searcher.search(query, limit=None)  # Get all search results
        #
        project_ids = [r["title"] for r in results]
        return project_ids, results
