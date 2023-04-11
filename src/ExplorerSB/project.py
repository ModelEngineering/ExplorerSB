'''Abstraction for a project. Includes methods both for building project context and accessing it.'''

"""
Project context:
    Abstract
    Citation
    DOI
    PROJECT_ID (key)
    RUNID
    TITLE

Also writes project files to CACHE_DIR under the RUNID.
"""

"""
TO DO
1. How incorporate building the whoosh index?
2. Tests.

"""


import src.ExplorerSB.constants as cn
from src.ExplorerSB.summary_parser import SummaryParser
from src.ExplorerSB import util

import os
import pandas as pd
import requests
import shutil
import tellurium as te
import time
import typing
import zipfile


class Project(object):
    # Usage
    #     Building context
    #         Project.buildContext()
    # .   Using existing context
    #         project = Project(project_id)
    #         project.initialize()
    #
    # Class data
    PROJECT_DCT = None # Used to build context
    PROJECT_IDS = None # Used to build context
    PROJECT_DF = None  # Used to exploit existing context

    def __init__(self, project_id: str):
        """
        Creates the context entry for a project.

        Args:
            project (Project)
        """
        self.summary_parsers = None
        # Context. Attribute names must be the same as in cn.CONTEXT_KEYS
        self.abstract = None
        self.citation = None
        self.doi = None
        self.paper_url = None
        self.project_id = project_id
        self.runid = None
        self.title = None

    ######################## 
    # Common Methods
    ######################## 
    def getCacheDirectory(self)->str:
        """
        Finds the path to the file cache for this project.

        Returns:
            file path
        """
        return os.path.join(cn.CACHE_DIR, self.runid)
    
    def getOutputsDirectory(self)->str:
        cache_path = self.getCacheDirectory()
        return os.path.join(cache_path, "outputs")

    ######################## 
    # Context building methods
    ######################## 
    def buildProject(self):
        """
        Constructs the context entry for a project

        Returns:
            dict: key, value for each context entry
        """
        # Handle class initialization
        if self.PROJECT_DCT is None:
            self.initializeClass()
        #
        summary_parser = SummaryParser(self.project_id)
        summary_parser.do()
        self.abstract = summary_parser.abstract
        self.citation = summary_parser.citation
        self.title = summary_parser.title
        self.doi = summary_parser.doi
        self.paper_url = summary_parser.paper_url
        self.runid = self._getRunid()
        #
        self._copyUrlFiles

    def _copyUrlFiles(self, dir_path:str=cn.CACHE_DIR)->typing.List[str]:
        """
        Copies the files to the Cache

        Args:
            dir_path: path to the parent directory destination directory

        Returns:
            list of paths copied
        """
        copied_paths = []
        dir_path = self.getCacheDirectory()
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        file_urls = self._getUrlFileList()
        for file_url in file_urls:
            path = self._copyUrlFile(file_url, dir_path=dir_path)
            if path is not None:
                copied_paths.append(path)
        return copied_paths
            
    def _getRunid(self)->str:
        dct = self.PROJECT_DCT[self.project_id]
        return dct["simulationRun"]
    
    def _getUrlFileList(self)->typing.List[str]:
        """
        Gets the list of file URLs for the project.

        Returns:
            list of URLs for project files
        """
        """
        Writes the files for this runid to the cache.

        Returns
        -------
        list-str (each string is a URL)
        """
        url = cn.API_URL + "/files/" + self.runid
        _, _, response_lst = util.readBiosimulations(url)
        file_urls = [x["url"] for x in response_lst]
        return file_urls
    
    def _downloadOutput(self)->str:
        """
        Downloads the output file and unzips it.

        Returns:
            path to the directory
        """
        url = "%s/results/%s/download" % (cn.API_URL, self.runid)
        try:
            response, _, _ = util.readBiosimulations(url, allow_redirects=True)
        except Exception as exp:
            import pdb; pdb.set_trace()
            print("\n**Could not access %s" % url)
            return
        # Unzip the file
        cache_path = self.getCacheDirectory()
        output_path = self.getOutputsDirectory()
        if os.path.isdir(output_path):
            shutil.rmtree(output_path)
        zip_path = os.path.join(cache_path, "output.zip")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(cache_path)
        #
        return output_path

    @classmethod
    def initializeClass(cls):
        """
        Initializes values of the project ids
        """
        response = requests.get(cn.PROJECT_URL)
        project_descs = response.json()
        cls.PROJECT_DCT = {d["id"]: d for d in project_descs}
        cls.PROJECT_IDS = list(cls.PROJECT_DCT.keys())

    def _copyUrlFile(self, file_url:str, dir_path:str)->str:
        """
        Copies the file in the URL to the specified directory for the runid.

        Args:
            file_url: URL to the file
            dir_path: Local directory in which file is placed

        Returns:
            path of copied file
        """
        try:
            response, _, _ = util.readBiosimulations(file_url, allow_redirects=True)
        except:
            print("\n**Could not access %s" % file_url)
            return
        filename = util.getFilenameFromUrl(file_url)
        output_path = os.path.join(dir_path, filename)
        with open(output_path, 'wb') as fd:
            fd.write(response.content)
        return output_path

    @classmethod
    def buildContext(cls, out_path=cn.CONTEXT_FILE, report_interval:int=5, first:int=0, last:int=None, sleep_sec:float=0):
        """
        Builds context for all projects. Writes the result to the context file

        Args:
            out_path: path for the output csv file
            report_interval: projects processed between prints
            first: first project to process
            last: last project to proces
            sleep_sec: delay between each iteration
        Returns:
            pd.DataFrame
        """
        if cls.PROJECT_DCT is None:
            cls.initializeClass()
        if last is None:
            last = 1e6
        # Check for an existing file
        if os.path.isfile(out_path):
            context_df = pd.read_csv(out_path, index_col=0)
            completed_project_ids = list(context_df.index)
        else:
            completed_project_ids = []
            context_df = pd.DataFrame()
        #
        dct = {k: [] for k in cn.CONTEXT_KEYS}
        for count, project_id in enumerate(cls.PROJECT_IDS):
            if project_id in completed_project_ids:
                continue
            if count < first:
                continue
            if count > last:
                continue
            project = Project(project_id)
            project.buildProject()
            for key in cn.CONTEXT_KEYS:
                dct[key].append(project.__getattribute__(key))
            #
            df = pd.DataFrame(dct)
            df = df.set_index(cn.PROJECT_ID)
            df = pd.concat([context_df, df])
            df.to_csv(out_path, index=True)
            _ = project._copyUrlFiles()
            project._downloadOutput()  # Download the output files
            total = count + 1
            if count % report_interval == 0:
                print("** Processed %d projects" % total)
            completed_project_ids.append(project_id)
            if sleep_sec > 0:
                if cn.CHATGPT_HEADER in project.abstract:
                    time.sleep(sleep_sec)
        #
        return df

    ######################## 
    # Context access methods
    ######################## 
    def initialize(self, context_file=cn.CONTEXT_FILE)->None:
        """
        Initializes previously built context
        """
        cls = self.__class__
        if cls.PROJECT_DF is None:
            cls.PROJECT_DF = pd.read_csv(context_file, index_col=0)
        #
        cls.PROJECT_IDS = list(cls.PROJECT_DF.index)
        for idx, key in enumerate(cn.CONTEXT_KEYS):
            if key != cn.PROJECT_ID:
                self.__setattr__(key, cls.PROJECT_DF.loc[self.project_id, key])

    def getFilePaths(self)->typing.List[str]:
        """
        Lists all locally stored files for the project
        """
        path_dir = self.getCacheDirectory()
        ffiles = []
        for ffile in os.listdir(path_dir):
            file_path = os.path.join(path_dir, ffile)
            if os.path.isfile(file_path):
                ffiles.append(file_path)
        return ffiles
    
    def generateModelAndData(self, is_write=True)->pd.DataFrame:
        """
        Runs a simulation if there is an SBML file. Puts the antimony file
        and the simulation results in the cache: model.ant, simulation_data.csv

        Args:
            is_write: write the model and data to the cache

        Returns:
            str: antimony model
            pd.DataFrame: index is time, columns are species
        """
        # See if there is an SBML file
        paths = self.getFilePaths()
        sbml_path = None
        for path in paths:
            splits = os.path.splitext(path)
            if splits[1] == ".xml":
                with open(path, "r") as fd:
                    lines = fd.readlines()
                model = "\n".join(lines)
                if not "sbml" in model:
                    continue
                sbml_path = path
                break
        #
        df = None
        antimony_str = None
        if sbml_path is not None:
            print("*** Simulating file %s" % path)
            try:
                rr = te.loadSBMLModel(model)
                antimony_str = rr.getAntimony()
                import pdb; pdb.set_trace()
                data = rr.simulate()
                df = pd.DataFrame(data, columns=data.colnames)
                df = df.set_index(df["time"])
                dir_path = self.getCacheDirectory()
                data_path = os.path.join(dir_path, "simulation_data.csv")
                antimony_path = os.path.join(dir_path, "model.ant")
                df.to_csv(data_path, index=True)
                with open(antimony_path, "w") as fd:
                    fd.writelines(antimony_str)
            except:
                print("*** Could not simulate file %s" % path)
        return antimony_str, df

    @classmethod 
    def iterateProjects(cls):
        """
        Iterates across all projects.

        Yields:
            Iterator[Project]: initialized project.
        """
        if cls.PROJECT_IDS is None:
            cls.initializeClass()
        for project_id in cls.PROJECT_IDS:
            project = Project(project_id)
            project.initialize()
            yield project

    def getH5FilePath(self)->str:
        """
        Provide the path to the HDF5 output file.

        Returns:
            path to file
        """
        output_dir = self.getOutputsDirectory()
        return os.path.join(output_dir, "reports.h5")