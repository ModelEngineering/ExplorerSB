'''Reads data created by ProjectBuilder'''

"""
Conventions:
    In general, the key for a dictionary is the project_id.
    Dictionaries with an "inv" prefix, have a value of project_id.
"""


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util
from src.ExplorerSB.corpus_manager import CorpusManager

from io import StringIO
import os
import pandas as pd
import plotly
import plotly.graph_objs as go
import tellurium as te
import tempdir
import tempfile
import typing
import zipfile

CORPUS_MANAGER = CorpusManager()


class ProjectReader():

    def __init__(self, project_id: str, data_dir:str=cn.DATA_DIR):
        """
        Creates the context entry for a project.

        Args:
            project_id: unique identifier for a project
            data_dir: directory in which project context is stored
        """
        self.corpus_manager = CORPUS_MANAGER
        for idx, key in enumerate(cn.CONTEXT_KEYS):
            if key != cn.PROJECT_ID:
                try:
                    self.__setattr__(key, self.corpus_manager.project_df.loc[project_id, key])
                except Exception as exp:
                    raise RuntimeError("Missing key %s:" % key)

    def _getZipDirPath(self):
        return os.path.join(self.data_dir, cn.ZIP_PAT % self.runid)
    
    def listFiles(self)->typing.List[str]:
        """
        Creates a list of the files present in the project zip.
        """
        zip_file = self._getZipDirPath()
        with zipfile.ZipFile(zip_file,'r') as zip:
            ffiles = zip.namelist()
        return ffiles

    def getFile(self, filename:str)->str:
        """
        Obtains the contents of a file in the cache for this project.

        Args:
            filename with extension

        Returns:
            str
        """
        zip_path = self._getZipFilePath()
        ffiles = self.listFiles()
        if not filename in ffiles:
            raise ValueError("File %s not found in %s" % (filename, zip_path))
        with zipfile.ZipFile(zip_file,'r') as zip:
            with zip.open(filename) as myfile:
                csv_bytes = zip.read(myfile)
        return csv_bytes.decode()
    
    @classmethod 
    def iterateProjects(cls, ignored_project_ids:typing.List[str]=None,
                        first:int=0, last:int=None, report_interval:int=None):
        """
        Iterates across all projects.
        Args:
            ignored_project_ids: project_ids that are ignored
            first: index of first project
            last: index of last project
            report_interval: how often to print progress
        Yields:
            Iterator[ProjectReader]: initialized project.
        """
        if cls.PROJECT_DF is None:
            raise RuntimeError("PROJECT_DF is not initialized!")
        if last is None:
            last = len(cls.PROJECT_IDS) + 1
        if report_interval is None:
            report_interval = len(cls.PROJECT_IDS) + 1
        if ignored_project_ids is None:
            ignored_project_ids = []
        excluded_project_ids = list(ignored_project_ids)
        #
        for count, project_id in enumerate(cls.PROJECT_IDS):
            if project_id in excluded_project_ids:
                continue
            if count < first:
                continue
            if count > last:
                continue
            project = ProjectReader(project_id)
            project.initialize()
            excluded_project_ids.append(project_id)
            # Check if reporting
            total = count + 1
            if count % report_interval == 0:
                print("***Processed project id=%s, runid=%s (%d)."
                       % (project.project_id, project.runid, total))
            yield project