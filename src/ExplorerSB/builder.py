"""
Builds the projects for the ExplorerSB project.

1. Projects are downloaded locally into a staging directory (stage_dir)
2. These files are processed:
    a. CSV files are created from h5 files using labels defined in the SEDML file
    b. The model file is extracted and converted to antimony
3. zip archives are created in the data directory (data_dir) that contains the following:
    a. CSV files
    b. Antimony files
    c. .png files

"""

import src.ExplorerSB.constants as cn
from src.ExplorerSB.project_builder import ProjectBuilder

import os
import pandas as pd
import requests
import time
import typing
import zipfile

"""
To Do

1. Subset the files copied to the data directory
2. Tests
"""

class Builder(object):

    def __init__(self, project_specification_csv:str=None, stage_dir:str=cn.STAGE_DIR, data_dir:str=cn.DATA_DIR, 
                 context_path:str=cn.CONTEXT_FILE,
                 first:int=0, last:int=None,
                 report_interval:int=5, sleep_sec:float=2, is_reset=True):
        """Constructor.

        Args:
            project_specification_csv (:obj:`str`, optional): path to CSV file with list of specific projects
            stage_dir: directory where intermediate files are stored
            data_dir (:obj:`str`, optional): directory where final files are stored
            context_path (:obj:`str`, optional): path to context file
            first: first project to process
            last: last project to process
            report_interval: projects processed between prints
            sleep_sec: delay between each iteration
        """
        self.project_specification_csv = project_specification_csv
        self.stage_dir = stage_dir
        self.data_dir = data_dir
        self.context_path = context_path
        self.first = first 
        self.last = last
        if self.last is None:
            self.last = 1e6
        self.report_interval = report_interval
        self.sleep_sec = sleep_sec
        #
        self.project_ids = None
        self.runid_dct = None
        #
        if is_reset:
            if os.path.isfile(self.context_path):
                os.remove(ffile)

    def _initialize(self):
        """
        Called after constructor to initialize the project ids and runids.
        """
        if self.project_specification_csv is not None:
            df = pd.read_csv(self.project_specification_csv)
            self.project_ids = df[cn.PROJECT_ID].tolist()
            self.runid_dct = {k: v for k, v in zip(self.project_ids, df[cn.RUNID].tolist())}
        else:
            response = requests.get(cn.PROJECT_URL)
            project_descs = response.json()
            dct = {d["id"]: d for d in project_descs}
            self.project_ids = list(dct.keys())
            # FIXME: Are these runids?
            self.runid_dct = {k: dct[k]["simulationRun"] for k in self.project_ids}

    def build(self):
        """
        Workflow for building project directories, context file, and creating zip files.
        The context file is built incrementally so that the process can be restarted, continuing from where it left off.
        """
        self._initialize()  # Get the project Ids and runids
        import pdb; pdb.set_trace()
        if os.path.isfile(self.context_path):
            context_df = pd.read_csv(self.context_path, index_col=0)
            context_dct = {k: context_df[k].tolist() for k in cn.CONTEXT_KEYS}
            context_df = context_df.set_index(cn.PROJECT_ID)
            msg = "***%d projects already built. See %s.\n" % (len(context_df), self.context_path)
            print(msg)
        else:
            context_dct = {k: [] for k in cn.CONTEXT_KEYS}
            context_df = pd.DataFrame(context_dct)
        for project_id, runid in self.runid_dct.items():
            if project_id in context_df.index:
                continue 
            print("** Processing %s" % project_id)
            builder = ProjectBuilder(project_id, runid, stage_dir=self.stage_dir, data_dir=self.data_dir)
            # Stage the project, create needed files, create the final project in the data directory
            builder.buildProject()
            # Get the context information
            for key in cn.CONTEXT_KEYS:
                context_dct[key].append(builder.__getattribute__(key))
            # Save context information
            df = pd.DataFrame(context_dct)
            df = df.set_index(cn.PROJECT_ID)
            df = pd.concat([context_df, df])
            df.to_csv(self.context_path, index=True)