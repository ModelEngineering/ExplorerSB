'''Obtains and parses the summary report for a project'''


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util
#from src.ExplorerSB.searcher import Searcher

import collections
from html.parser import HTMLParser
import numpy as np
import os
import requests
import typing

MINIMUM_DESCRIPTION_LENGTH = 50


######## Constants #######
BASE_PUBMED_URL = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"
QUERY_PAT = "?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:%07d&metadataPrefix=oai_dc"
URL_PAT = BASE_PUBMED_URL + QUERY_PAT
# Converting DOI to PMCID
PMCID_BASE_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
PMCID_PAT = PMCID_BASE_URL + "?tool=my_tool&email=my_email@example.com&ids=%s"
TEST_DOI = "10.1093/bioinformatics/btaa720"

MINIMUM_TITLE_LENGTH = 40
MAXIMUM_COMMA_IN_TITLE = 3

TextCoordinate = collections.namedtuple("TextCoordinate", "line char")

def extractText(text, start_coord, end_coord):
    """Extracts text from the specified coordinates

    Args:
        text (str):
        start_coord (TextCoordinate)
        end_coord (TextCoordinate)

    Returns:
        str
    """
    def findTextPosition(coord):
        """Finds the position of the text in the string"""
        pos = 0
        for i in range(coord.line):
            pos = text.index("\n", pos) + 1
        pos += coord.char
        return pos
    #
    start_pos = findTextPosition(start_coord)
    end_pos = findTextPosition(end_coord)
    return text[start_pos:end_pos]


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


class AbstractParser(HTMLParser):
# Parses for abstracts in the descriptions key
    def init(self):
        self.data = []  # List of data
        self.start_coord = None
        self.end_coord = None

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if "abstract" in self.get_starttag_text():
                self.start_coord = TextCoordinate(self.getpos()[0], self.getpos()[1])

    def handle_endtag(self, tag):
        if tag == "div":
            if (self.start_coord is not None) and (self.end_coord is None):
                self.end_coord = TextCoordinate(self.getpos()[0], self.getpos()[1]) 

    def handle_data(self, data):
        self.data.append(data)


class SummaryParser(object):

    def __init__(self, project_id, is_report=True, is_chatgpt=False):
        """
        Parameters
        ----------
        Args:
            project_id (str)
            is_report (bool): report an error, don't raise an exception
        """
        self.project_id = project_id
        self.is_report = is_report
        if is_chatgpt:
            raise NotImplementedError("ChatGPT usage is not implemented")
        #
        self.summary_dct = None
        #
        self.title = None
        self.abstract = None
        self.citation = None
        self.doi = None
        self.paper_url = None
    
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
        self.title, error_str = self._extractTitle()
        error_strs += error_str
        self.paper_url, error_str = self._getPaperUrl()
        error_strs += error_str
        self.abstract = self._getAbstract(self.doi, self.citation)
        if len(error_str) > 0:
            print("***%s" % error_str)

    def _extractDOI(self):
        raise NotImplementedError("Must be implemented by subclass")
    
    def _extractCitation(self):
        raise NotImplementedError("Must be implemented by subclass")
    
    def _extractTitle(self):
        raise NotImplementedError("Must be implemented by subclass")
    
    def _getPaperUrl(self):
        raise NotImplementedError("Must be implemented by subclass")
    
    def _getAbstract(self, *pargs):
        raise NotImplementedError("Must be implemented by subclass")


class BiosimulationsSummaryParser(SummaryParser):

    def __init__(self, project_id, is_report=True):
        """
        Parameters
        ----------
        Args:
            project_id (str)
            is_report (bool): report an error, don't raise an exception
        """
        super(BiosimulationsSummaryParser, self).__init__(project_id, is_report-is_report)
        self.summary_response = None
        self.summary_str = None
        self.description_html = None

    def _initialize(self):
        """
        Acquires the summary description from BioSimulations
        """
        url = "%s/projects/%s/summary" % (cn.API_URL, self.project_id)
        self.summary_response, self.summary_str, self.summary_dct = util.readBiosimulations(url)
        self.description_html = self.summary_dct["simulationRun"]["metadata"][0]['description']

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
    
    def _extractTitle(self)->list[str]:
        """
        Extracts the title from the citation.

        Returns:
            str: citation
            str: error message if null
        """
        self._check()
        text = self.citation
        if text is None:
            return "", "Citation not found; cannot calculate title."
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
    def _getAbstract(self, doi: str, citation: str) ->list[str]:
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
            if False:
                pass
                # if self.is_chatgpt:
                #     searcher = Searcher()
                #     abstract = searcher.get(citation)
                #     abstract = cn.CHATGPT_HEADER + abstract
            else:
                parser = AbstractParser()
                parser.init()
                parser.feed(self.description_html)
                if parser.start_coord is None:
                    if len(self.description_html) > MINIMUM_DESCRIPTION_LENGTH:
                        abstract = self.description_html
                    else:
                        abstract = ""
                        print ("***Abstract not found for %s" % self.project_id)
                else:
                    abstract = extractText(self.description_html, parser.start_coord, parser.end_coord)
                    abstract = abstract.replace("<p>", "")
                    abstract = abstract.replace("</p>", "")
                    abstract = abstract.replace("<div>", "")
                    abstract = abstract.replace("</div>", "")
        return abstract
    

class BiomodelsSummaryParser(BiosimulationsSummaryParser):

    def _initialize(self):
        """
        Acquires the summary description from BioSimulations
        """
        super(BiomodelsSummaryParser, self)._initialize()
        pos = self.project_id.index("_")
        self.biomodels_name = self.project_id[:pos] 
        self.summary_dct = util.getBiomodelInfo(self.biomodels_name)

    def _getAbstract(self, *pargs) ->list[str]:
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
        abstract = self.summary_dct["synopsis"]
        if abstract == "":
            import pdb; pdb.set_trace()
        return abstract
        
    def _extractCitation(self)->list[str]:
        """
        Calculates the citation

        Args:
            summary_dct (dcit): _description_

        Returns:
            str: citation string
            str: error message if citation is empty
        """
        citation = ""
        for key in ['authors', 'title', 'journal', 'year']:
            if key in self.summary_dct.keys():
                citation += str(self.summary_dct[key]) + " "
        return citation, ""

    def _extractTitle(self)->list[str]:
        """
        Extracts the title from the citation.

        Returns:
            str: citation
            str: error message if null
        """
        return self.summary_dct["title"], ""
    
    def _getPaperUrl(self)->str:
        """
        Extracts the paper URL.

        Returns:
            str
        """
        return self.summary_dct["link"], ""