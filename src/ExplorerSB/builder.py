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
import src.ExplorerSB.util as util
from src.ExplorerSB.project_builder import ProjectBuilder

import json
import os
import pandas as pd
import requests
import time
import typing
import zipfile


class Builder(object):

    def __init__(self, project_specification_csv:str=None, stage_dir:str=cn.STAGE_DIR, data_dir:str=cn.DATA_DIR, 
                 first:int=0, last:int=None,
                 report_interval:int=5, sleep_sec:float=2, is_reset=True):
        """Constructor.

        Args:
            project_specification_csv (:obj:`str`, optional): path to CSV file with list of specific projects
            stage_dir: directory where intermediate files are stored
            data_dir (:obj:`str`, optional): directory where final files are stored
            first: first project to process
            last: last project to process
            report_interval: projects processed between prints
            sleep_sec: delay between each iteration
        """
        self.project_specification_csv = project_specification_csv
        self.stage_dir = stage_dir
        self.data_dir = data_dir
        self.csv_context_path = os.path.join(self.data_dir, cn.CONTEXT_FILE_NAME + ".csv")
        self.json_context_path = os.path.join(self.data_dir, cn.CONTEXT_FILE_NAME + ".json")
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
            for ffile in [self.csv_context_path, self.json_context_path]:
                if os.path.isfile(ffile):
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
        if os.path.isfile(self.csv_context_path):
            context_df = pd.read_csv(self.csv_context_path)
            context_df = context_df.drop_duplicates()
            context_dct = {k: context_df[k].tolist() for k in cn.CONTEXT_KEYS}
            msg = "\n\n***%d projects already built. See %s.\n" % (len(context_df), self.csv_context_path)
            print(msg)
        else:
            context_dct = {k: [] for k in cn.CONTEXT_KEYS}
        util.trace("Completed setup", 1)
        zip_files = [f for f in os.listdir(self.data_dir) if f.endswith(".zip")]
        # Do not re-process projects for which there are already a zip file 
        for project_id, runid in self.runid_dct.items():
            zip_file = "%s.zip" % runid
            if (zip_file in zip_files) and (project_id in context_dct[cn.PROJECT_ID]):
                print("***Skipping %s because it already exists." % project_id)
                continue
            if project_id cn.SKIP_PROJECT_IDS:
                print("***Skipping %s in constants.SKIP_PROJECT_IDS." % project_id)
                continue
            print("** Processing %s" % project_id)
            builder = ProjectBuilder(project_id, runid, stage_dir=self.stage_dir, data_dir=self.data_dir)
            util.trace("Constructed builder", 1)
            if not builder.is_biomodels:
                print("***Skipping %s. Not BIOMODELS." % project_id)
                continue
            # Stage the project, create needed files, create the final project in the data directory
            builder.buildProject()
            util.trace("Built project", 1)
            # Save the context information as json and csv
            for key in cn.CONTEXT_KEYS:
                context_dct[key].append(builder.__getattribute__(key))
            # Save context information
            df = pd.DataFrame(context_dct)
            ffile_json = df.to_json(orient="records", indent=4)
            with open(self.json_context_path, "w") as fd:
                fd.write(ffile_json)
            df = df.set_index(cn.PROJECT_ID)
            df.to_csv(self.csv_context_path, index=True)
            util.trace("Saved context information", 2)