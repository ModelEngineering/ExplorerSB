"""Obtains abstracts from pubmed"""
"""
Builds a CSV file with the fields:
    project_id
    citation
    abstract
"""

import src.ModelExplorerSB.constants as cn
from src.ModelExplorerSB.searcher import Searcher

from html.parser import HTMLParser
import os
import pandas as pd
import requests
import typing


BASE_PUBMED_URL = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"
QUERY_PAT = "?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:%07d&metadataPrefix=oai_dc"
URL_PAT = BASE_PUBMED_URL + QUERY_PAT
# Converting DOI to PCMID
PCMID_BASE_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
PCMID_PAT = PCMID_BASE_URL + "?tool=my_tool&email=my_email@example.com&ids=%s"
TEST_DOI = "10.1093/bioinformatics/btaa720"
CHATGPT_HEADER = """
Abstract not found in PubMed. The following is obtained from ChatGPT.

"""
MINIMUM_TITLE_LENGTH = 40
MAXIMUM_COMMA_IN_TITLE = 3


#-------------- CLASSES--------------#
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


#-------------- FUNCTIONS --------------#
def extractPmcids(response: requests.models.Response) -> list[str]:
        """
        Extracts PMCIDs from the response to a conversion query.

        Parameters
        ----------
        response:

        Returns
        -------
        pmcids
        """
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

def extractAbstract(pmcid: str) ->list[str]:
        """
        Obtains the abstract for the article. Since tags may differ for articles
        returns the longest data.

        Parameters
        ----------
        pmcid: str

        Returns
        -------
        list-str
        """
        digits = int(pmcid[3:])
        query_url = URL_PAT % digits
        response = requests.get(query_url)
        parser = DataParser()
        parser.init()
        parser.feed(response.content.decode())
        data = sorted(parser.data, key=lambda d: len(d), reverse=True)
        return data[0]

def getAbstract(doi: str) -> str:
    """
    Finds the abstract for an article.

    Parameters
    ----------
    doi: doi string for article

    Returns
    -------
    abstract
    """
    # Convert DOI to PCMID
    query_url = PCMID_PAT % doi
    response = requests.get(query_url)
    pmcids = extractPmcids(response)
    if len(pmcids) > 0:
        abstract = extractAbstract(pmcids[0])
    else:
        abstract = ""
        print ("*** No pmcid found for doi %s" % doi)
    return abstract

def buildAbstracts(start_idx:int=0, max_process:int=-1,
                   output_path:str=cn.ABSTRACT_FILE,
                   report_interval:int=5)->pd.DataFrame:
    """
    Scraps abstracts for models in Biosimulations.

    Parameters
    ----------
    start_idx: int (index to start for processing)
    max_process: int (maximum number to process)
    output_path: path to CSV with results
    report_interval: report every <n> itereations

    Returns
    -------
    pd.DataFrame
    """
    def extractDoi(response_str:str, key:str)->str:
        if key in response_str:
            pos = response_str.index(key)
        else:
            return None
        start_pos = pos + len(key)
        end_pos = response_str[start_pos:].index('"') + start_pos
        doi = response_str[start_pos:end_pos]
        return doi
    #
    # Get the list of projects
    response = requests.get(cn.PROJECT_URL)
    project_descs = response.json()
    project_dct = {d[cn.ID]: d for d in project_descs}
    project_ids = list(project_dct.keys())
    # Iterate over project to extract information
    searcher = Searcher()
    abstract_dct = {cn.ID: [], cn.CITATION: [],
           cn.ABSTRACT: [], cn.DOI: [], cn.TITLE: []}
    if os.path.isfile(output_path):
        base_df = pd.read_csv(output_path)
        processed_ids = set(base_df[cn.ID])
    else:
        base_df = pd.DataFrame()
        processed_ids = set([])
    for idx, pid in enumerate(project_ids):
        if (idx < start_idx) or (pid in processed_ids):
            continue
        summary_url = "%s/projects/%s/summary" % (cn.API_URL, pid)
        response = requests.get(summary_url)
        null = None
        dct = eval(response.content.decode())
        if len(dct["simulationRun"]["metadata"]) == 0:
            print("*** No citation in %s" % pid)
            continue
        if len(dct["simulationRun"]["metadata"][0]["citations"]) == 0:
            print("*** No citation in %s" % pid)
            continue
        #
        citation = dct["simulationRun"]["metadata"][0]["citations"][0]["label"]
        # Title
        text = citation
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
                print ("*** Title not found in %s" % pid)
                title = ""
                break
        # Extract the DOI
        response_str = response.content.decode()
        for key in ["/doi:", "doi/"]:
            doi = extractDoi(response_str, key)
            if doi is not None:
                break
        if doi is None:
            print("*** No DOI found in %s" % pid)
            continue
        # Get the abstract
        abstract = getAbstract(doi)
        if len(abstract) == 0:
            abstract = searcher.get(citation)
            abstract = CHATGPT_HEADER + abstract
        # Update the data
        abstract_dct[cn.ID].append(pid)
        abstract_dct[cn.CITATION].append(citation)
        abstract_dct[cn.ABSTRACT].append(abstract)
        abstract_dct[cn.DOI].append(doi)
        abstract_dct[cn.TITLE].append(title)
        if idx % 5 == 0:
            print(idx)
        if max_process >= 0:
            if idx >= max_process-1:
                break
        #
        df = pd.DataFrame(abstract_dct)
        full_df = pd.concat([base_df, df])
        full_df.index = range(len(full_df))
        for column in full_df.columns:
            if "Unnamed:" in column:
                del full_df[column]
        full_df.to_csv(output_path)
    return df

if __name__ == '__main__':
    result = buildAbstracts()
