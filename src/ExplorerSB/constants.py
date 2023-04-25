'''Builds the context and index information needed for the runtime UI.'''



import os

# Environment: indicates if running in GitHub actions
if "IS_GITHUB" in os.environ.keys():
    IS_GITHUB = True
else:
    IS_GITHUB = False



# Directories
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(PROJECT_DIR)
LOCAL_DIR = os.path.join(PROJECT_DIR, "local")
TEST_DIR = os.path.join(PROJECT_DIR, "tests")
DATA_DIR = os.path.join(PROJECT_DIR, "data")
INDEX_DIR = os.path.join(DATA_DIR, "indexdir")
ABSTRACT_FILE = os.path.join(INDEX_DIR, "abstracts.csv")
APIKEY_FILE = os.path.join(LOCAL_DIR, "apikey.txt")
CACHE_DIR = os.path.join(DATA_DIR, "cache")
CONTEXT_FILE = os.path.join(DATA_DIR, "context.csv")
# File types
CELLML = "cellml"
CSV = "csv"
SEDML = "sedml"
XML = "xml"
# Archive files
ANT_ZIP = os.path.join(DATA_DIR, "ant.zip")
CELLML_ZIP = os.path.join(DATA_DIR, "cellml.zip")
CSV_ZIP = os.path.join(DATA_DIR, "csv.zip")
SEDML_ZIP = os.path.join(DATA_DIR, "sedml.zip")
XML_ZIP = os.path.join(DATA_DIR, "xml.zip")

# URLs
API_URL = "https://api.biosimulations.org"
PROJECT_URL = "%s/projects" % API_URL

# Fields in context.csv
ABSTRACT = "abstract"
CITATION = "citation"
DOI = "doi"
PAPER_URL = "paper_url"
PROJECT_ID = "project_id"
TITLE = "title"
RUNID = "runid"
CONTEXT_KEYS = [ABSTRACT, CITATION, DOI, PAPER_URL, PROJECT_ID, RUNID, TITLE]

#
CHATGPT_HEADER = """
Abstract not found in PubMed. The following is obtained from ChatGPT.

"""
NAME_SEPARATOR = "--"