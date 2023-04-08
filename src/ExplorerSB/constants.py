import os

# Environment: indicates if running in GitHub actions
if "IS_GITHUB" in os.environ.keys():
    IS_GITHUB = True
else:
    IS_GITHUB = False



# Directories
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(PROJECT_DIR)
TEST_DIR = os.path.join(PROJECT_DIR, "tests")
LOCAL_DIR = os.path.join(PROJECT_DIR, "local")
INDEX_DIR = os.path.join(LOCAL_DIR, "indexdir")
ABSTRACT_FILE = os.path.join(INDEX_DIR, "abstracts.csv")
APIKEY_FILE = os.path.join(LOCAL_DIR, "apikey.txt")
CACHE_DIR = os.path.join(LOCAL_DIR, "cache")
CONTEXT_FILE = os.path.join(LOCAL_DIR, "context.csv")

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