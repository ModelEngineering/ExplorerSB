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

    @property
    def short_title(self):
        if self.title is not None:
            if len(self.title) <= MAX_TITLE_LENGTH:
                return self.title
            else:
                return self.title[:MAX_TITLE_LENGTH] + "..."
        return None
  
    def getProjectCacheDirectory(self, is_create:bool=False)->str:
        """
        Finds the path to the file cache for this project.

        Args:
            is_create: create the directory if it does not exist

        Returns:
            file path
        """
        if self.runid is None:
            raise RuntimeError("Project is not initialized!")
        if (not os.path.isdir(self.data_dir)) and is_create:
            os.mkdir(self.data_dir)
        project_cache_dir = os.path.join(self.data_dir, self.runid)
        if (not os.path.isdir(project_cache_dir)) and (is_create):
            os.mkdir(project_cache_dir)
        return project_cache_dir
    
    def getFilePaths(self, **kwargs:dict)->typing.List[str]:
        """
        Lists all locally stored files for the project

        Args:
            kwargs: arguments to getProjectCacheDirectory
        """
        path_dir = self.getProjectCacheDirectory(**kwargs)
        ffiles = []
        if not os.path.isdir(path_dir):
            return ffiles
        for ffile in os.listdir(path_dir):
            file_path = os.path.join(path_dir, ffile)
            if os.path.isfile(file_path):
                ffiles.append(file_path)
        return ffiles