'''Obtains and parses the summary report for a project'''


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util
from src.ExplorerSB.searcher import Searcher

from htmldom import htmldom
from html.parser import HTMLParser
from requests_html import HTMLSession
import numpy as np
import os
import requests
import typing



######## Constants #######
BASE_PUBMED_URL = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"
QUERY_PAT = "?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:%07d&metadataPrefix=oai_dc"
URL_PAT = BASE_PUBMED_URL + QUERY_PAT
# Converting DOI to PMCID
PMCID_BASE_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
PMCID_PAT = PMCID_BASE_URL + "?tool=my_tool&email=my_email@example.com&ids=%s"
TEST_DOI = "10.1093/bioinformatics/btaa720"
CHATGPT_HEADER = """
Abstract not found in PubMed. The following is obtained from ChatGPT.

"""
MINIMUM_TITLE_LENGTH = 40
MAXIMUM_COMMA_IN_TITLE = 3


######################################################################
# CLASSES
######################################################################
class GenericParser(HTMLParser):
# Parses all tags into a dictionary of tags with a dictionary of attributes

    def init(self):
        self.data_dct = {}

    def handle_starttag(self, tag, attrs):
        if not tag in self.data_dct.keys():
            self.data_dct[tag] = []
        dct = {k: v for (k, v) in attrs}
        self.data_dct[tag].append(dct)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


class DataParser(HTMLParser):
# Parses all data into a dictionary indexed by data length
    def init(self):
        self.data = []  # List of data

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        self.data.append(data)


class SummaryParser(object):

    def __init__(self, project_id, is_report=True):
        """
        Parameters
        ----------
        Args:
            project_id (str)
            is_report (bool): report an error, don't raise an exception
        """
        self.project_id = project_id
        self.is_report = is_report
        #
        self.summary_response = None
        self.summary_str = None
        self.summary_dct = None
        #
        self.title = None
        self.abstract = None
        self.citation = None
        self.doi = None
        self.paper_url = None

    def _initialize(self):
        """
        Acquires the summary description from BioSimulations
        """
        url = "%s/projects/%s/summary" % (cn.API_URL, self.project_id)
        self.summary_response, self.summary_str, self.summary_dct = util.readBiosimulations(url)

    def _check(self):
        if self.summary_str is None:
            raise RuntimeError("Must call _initialize before running this method.")

    def do(self): 
        """
        Build the summary data
        """
        self._initialize()
        #
        error_strs = ""
        self.doi, error_str = self._extractDOI()
        error_strs += error_str
        self.citation, error_str = self._extractCitation()
        error_strs += error_str
        self.title, error_str = self._extractTitle(self.citation)
        error_strs += error_str
        self.paper_url, error_str = self._getPaperUrl()
        error_strs += error_str
        self.abstract = self._getAbstract(self.doi, self.citation)
        if len(error_str) > 0:
            print("***%s" % error_str)

    
    def _extractDOI(self)->typing.Tuple[str, str]:
        """
        Extracts the DOI from the response to a summary REST call.

        Returns:
            str: citation
            str: error string
        """
        self._check()
        def extract(key):
            if key in self.summary_str:
                pos = self.summary_str.index(key)
                start_pos = pos + len(key)
                end_pos = self.summary_str[start_pos:].index('"') + start_pos
                doi = self.summary_str[start_pos:end_pos]
                return doi
            else:
                return ""
        #
        for key in ["/doi:", "doi/"]:
            doi = extract(key)
            if len(doi) > 0:
                return  doi, ""
        #
        error_str = "DOI not found"
        if not self.is_report:
            raise RuntimeError(error_str)
        return "", error_str
        
    def _extractCitation(self)->list[str]:
        """
        Calculates the citation

        Args:
            summary_dct (dcit): _description_

        Returns:
            str: citation string
            str: error message if citation is empty
        """
        self._check()
        citation = None
        is_error = False
        is_metadata = len(self.summary_dct["simulationRun"]["metadata"]) > 0
        if is_metadata:
            if len(self.summary_dct["simulationRun"]["metadata"][0]["citations"]) > 0:
                citation = self.summary_dct["simulationRun"]["metadata"][0]["citations"][0]["label"]
            else:
                is_error = True
        else:
            is_error = True
        if is_error:
            error_str = "No citation found."
        else:
            error_str = ""
        #
        if (len(error_str) > 0) and (not self.is_report):
            raise RuntimeError(error_str)
        return citation, error_str
    
    def _extractTitle(self, citation)->list[str]:
        """
        Extracts the title from the citation.

        Returns:
            str: citation
            str: error message if null
        """
        self._check()
        text = citation
        is_error = False
        while len(text) > 0:
            try:
                start_pos = text.index(".") + 1
                text = text[start_pos:]
                end_pos = text.index(".")
                title = text[:end_pos]
                if (len(title) > MINIMUM_TITLE_LENGTH)  \
                      and text.count(",") <= MAXIMUM_COMMA_IN_TITLE:
                    break
                text = text[end_pos:]
            except ValueError:
                title = ""
                is_error = True
                break
        if is_error:
            error_str =  "Title not found in %s" % self.project_id
        else:
            error_str = ""
        #
        if (len(error_str) > 0) and (not self.is_report):
            raise RuntimeError(error_str)
        return title, error_str
    
    def _getPaperUrl(self)->str:
        """
        Extracts the paper URL.

        Returns:
            str
        """
        self._check()
        paper_url = util.setValue(util.indexNested(self.summary_dct,
          ["simulationRun", "metadata", 0, "citations", 0, "uri"]), None)
        if paper_url is None:
            return "", "No URI found."
        else:
            return paper_url, ""

    # FIXME: Find abstract inside the summary; handle no DOI
    @staticmethod
    def _getAbstract(doi: str, citation: str) ->list[str]:
        """
        Obtains the abstract for the article. Abstract may be obtained from:
            (1) inside the summary
            (2) PubMed
            (3) ChatGPT

        Args:
            doi: str
            citation: str
        Returns:
            list-str
        """
        def extractPmcids(response):
            # Find the pmcid
            parser = GenericParser()
            parser.init()
            parser.feed(response.content.decode())
            pmcids = []
            if "record" in parser.data_dct.keys():
                for record in parser.data_dct["record"]:
                    if "pmcid" in record.keys():
                        pmcids.append(record["pmcid"])
            #
            return pmcids
        #
        # Convert DOI to PMCID
        query_url = PMCID_PAT % doi
        response = requests.get(query_url)
        pmcids = extractPmcids(response)
        # If we have a pmcid, retrieve the abstract
        if len(pmcids) > 0:
            pmcid = pmcids[0]
            # Get the abstract from pubmed
            digits = int(pmcid[3:])
            query_url = URL_PAT % digits
            response = requests.get(query_url)
            parser = DataParser()
            parser.init()
            parser.feed(response.content.decode())
            data = sorted(parser.data, key=lambda d: len(d), reverse=True)
            abstract = data[0]
        else:
            searcher = Searcher()
            abstract = searcher.get(citation)
            abstract = CHATGPT_HEADER + abstract
        return abstract