'''Base abstraction for a project.'''

"""
Conventions:
    In general, the key for a dictionary is the project_id.
    Dictionaries with an "inv" prefix, have a value of project_id.
"""


import src.ExplorerSB.constants as cn

import os
import pandas as pd
import typing

MAX_TITLE_LENGTH = 100


class ProjectBase(object):


    def __init__(self, project_id: str, data_dir:str=cn.DATA_DIR):
        """
        Creates the context entry for a project.

        Args:
            project_id: unique identifier for a project
            data_dir: directory in which project context is stored
        """
        self.data_dir = data_dir
        self.summary_parsers = None
        self.abstract = None
        self.citation = None
        self.doi = None
        self.project_id = project_id
        self.paper_url = None
        self.runid = None
        self.title = None
        self.is_biomodels = "BIOMD" in project_id.upper()

    @property
    def short_title(self):
        if self.title is not None:
            if len(self.title) <= MAX_TITLE_LENGTH:
                return self.title
            else:
                return self.title[:MAX_TITLE_LENGTH] + "..."
        return None
  
    def getProjectDir(self, dest_dir:str, is_create:bool=False)->str:
        """
        Finds the path to the file cache for this project.

        Args:
            is_create: create the directory if it does not exist
            dest_dir: directory in which project cache is stored

        Returns:
            file path
        """
        if (not os.path.isdir(dest_dir)) and is_create:
            os.mkdir(dest_dir)
        project_dir = os.path.join(dest_dir, self.runid)
        if (not os.path.isdir(project_dir)) and (is_create):
            os.mkdir(project_dir)
        return project_dir
    
    def getFilePaths(self, dest_dir)->typing.List[str]:
        """
        Lists all locally stored files for the project

        Args:
            dest_dir: directory to search
        """
        path_dir = self.getProjectDir(dest_dir)
        ffiles = []
        if not os.path.isdir(path_dir):
            return ffiles
        for ffile in os.listdir(path_dir):
            file_path = os.path.join(path_dir, ffile)
            if os.path.isfile(file_path):
                ffiles.append(file_path)
        return ffiles