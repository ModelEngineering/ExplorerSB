import os

# Directories
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(PROJECT_DIR)
TEST_DIR = os.path.join(PROJECT_DIR, "tests")
INDEX_DIR = os.path.join(PROJECT_DIR, "indexdir")
ABSTRACT_FILE = os.path.join(INDEX_DIR, "abstracts.csv")
LOCAL_DIR = os.path.join(PROJECT_DIR, "local")
APIKEY_FILE = os.path.join(LOCAL_DIR, "apikey.txt")
CACHE_DIR = os.path.join(PROJECT_DIR, "cache")

# URLs
API_URL = "https://api.biosimulations.org"
PROJECT_URL = "%s/projects" % API_URL

# Fields
ABSTRACT = "abstract"
CITATION = "citation"
DOI = "doi"
ID = "id"
TITLE = "title"
