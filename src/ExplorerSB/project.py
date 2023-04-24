'''Abstraction for a project. Uses data produced by ProjectBuild'''

"""
Conventions:
    In general, the key for a dictionary is the project_id.
    Dictionaries with an "inv" prefix, have a value of project_id.
"""


import src.ExplorerSB.constants as cn
from src.ExplorerSB.project_base import ProjectBase

import os
import pandas as pd
import requests
import shutil
import tellurium as te
import time
import typing


class Project(ProjectBase):

    PROJECT_IDS = None
    PROJECT_DF = None  # Dataframe describing projects. Columns are:
        #ABSTRACT 
        #CITATION 
        #DOI 
        #PAPER_URL 
        #PROJECT_DF 
        #PROJECT_ID 
        #RUNID 
        #TITLE
    INV_TITLE_DCT = None
    INV_SHORT_TITLE_DCT = None

    def __init__(self, project_id: str, data_dir:str=cn.DATA_DIR):
        """
        Creates the context entry for a project.

        Args:
            project_id: unique identifier for a project
            data_dir: directory in which project context is stored
        """
        super().__init__(project_id, data_dir=data_dir)

    @classmethod
    def resetClassAttributes(cls):
        cls.PROJECT_IDS = None
        cls.PROJECT_DF = None
        cls.INV_TITLE_DCT = None
        cls.INV_SHORT_TITLE_DCT = None


    @classmethod
    def initializeClass(cls):
        if cls.PROJECT_DF is not None:
            return
        # Get the project dataframe for projects with titles
        cls.PROJECT_DF = pd.read_csv(cn.CONTEXT_FILE, index_col=0)
        sel_with_title = [isinstance(t, str) for t in cls.PROJECT_DF[cn.TITLE]]
        cls.PROJECT_DF = cls.PROJECT_DF[sel_with_title]
        cls.PROJECT_DF[cn.TITLE] = [t.strip() for t in cls.PROJECT_DF[cn.TITLE]]
        # Adjust for duplicate titles
        for idx, row in cls.PROJECT_DF.iterrows():
            pids = [p for p, t in zip(cls.PROJECT_DF.index, cls.PROJECT_DF[cn.TITLE]) if t == row[cn.TITLE]]
            if len(pids) > 1:
                for count, pid in enumerate(pids):
                    prefix = "(%d) " % (count + 1)
                    cls.PROJECT_DF.loc[pid, cn.TITLE] = prefix + cls.PROJECT_DF.loc[pid, cn.TITLE]
        # Create short titles
        projects = [Project(p) for p in cls.PROJECT_DF.index]
        [p.initialize() for p in projects]
        cls.INV_TITLE_DCT = {p.title: p.project_id for p in projects}
        cls.INV_SHORT_TITLE_DCT = {p.short_title: p.project_id for p in projects}
        cls.PROJECT_IDS = list(cls.PROJECT_DF.index)

    def initialize(self, context_file=cn.CONTEXT_FILE)->None:
        """
        Initializes project once the class is initialized.
        """
        cls = self.__class__
        cls.initializeClass()
        #
        for idx, key in enumerate(cn.CONTEXT_KEYS):
            if key != cn.PROJECT_ID:
                try:
                    self.__setattr__(key, cls.PROJECT_DF.loc[self.project_id, key])
                except Exception as exp:
                    import pdb; pdb.set_trace()
                    pass

    @classmethod 
    def findProjectByShortTitle(cls, short_title):
        """
        Finds the project with the provided short title.
        """
        cls.initializeClass()
        #
        if short_title in cls.INV_SHORT_TITLE_DCT.keys():
            return cls.INV_SHORT_TITLE_DCT[short_title]
        else:
            return None
    
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
            Iterator[Project]: initialized project.
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
            project = Project(project_id)
            project.initialize()
            excluded_project_ids.append(project_id)
            # Check if reporting
            total = count + 1
            if count % report_interval == 0:
                print("***Processed project id=%s, runid=%s (%d)."
                       % (project.project_id, project.runid, total))
            yield project
