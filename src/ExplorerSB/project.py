'''Abstraction for a project. Includes methods both for building project context and accessing it.'''

"""
Project context:
    Abstract
    Citation
    DOI
    PROJECT_ID (key)
    RUNID
    TITLE
    PAPER_URL

Also writes project files to CACHE_DIR under the RUNID.
"""


import src.ExplorerSB.constants as cn
from src.ExplorerSB.summary_parser import SummaryParser
from src.ExplorerSB import util

import h5py
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
        self.project_id = project_id
        self.paper_url = None
        self.runid = None
        self.title = None

    ######################## 
    # Common Methods
    ######################## 
    def getProjectCacheDirectory(self, cache_dir:str=None, is_create:bool=False)->str:
        """
        Finds the path to the file cache for this project.

        Args:
            cache_dir: directory for caching files
            is_create: create the directory if it does not exist

        Returns:
            file path
        """
        if cache_dir is None:
            cache_dir = cn.CACHE_DIR
        project_cache_dir = os.path.join(cache_dir, self.runid)
        if (not os.path.isdir(project_cache_dir)) and (is_create):
            os.mkdir(project_cache_dir)
        return project_cache_dir
    
    def getOutputsDirectory(self, cache_dir:str=None)->str:
        project_cache_dir = self.getProjectCacheDirectory(cache_dir=cache_dir)
        return os.path.join(project_cache_dir, "outputs")
    
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
        if cls.PROJECT_IDS is None:
            cls.initializeClass()
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

    def _copyUrlFiles(self, cache_dir:str=cn.CACHE_DIR)->typing.List[str]:
        """
        Copies the files to the Cache

        Args:
            cache_dir: path to the parent directory destination directory

        Returns:
            list of paths copied
        """
        copied_paths = []
        project_cache_dir = self.getProjectCacheDirectory()
        if not os.path.isdir(project_cache_dir):
            os.mkdir(project_cache_dir)
        file_urls = self._getUrlFileList()
        for file_url in file_urls:
            path = self._copyUrlFile(file_url, project_cache_dir)
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
    
    def _downloadOutput(self, cache_dir:str=None)->str:
        """
        Downloads the output file and unzips it.

        Args:
            cache_dir: path to cache directory

        Returns:
            path to the directory
        """
        LOCAL_FILENAME = "output.zip"
        url = "%s/results/%s/download" % (cn.API_URL, self.runid)
        project_cache_dir = self.getProjectCacheDirectory(cache_dir=cache_dir)
        _ = self._copyUrlFile(url, project_cache_dir, local_filename=LOCAL_FILENAME)
        zip_path = os.path.join(project_cache_dir, LOCAL_FILENAME)
        # Unzip the file
        output_dir = self.getOutputsDirectory(cache_dir=cache_dir)
        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(project_cache_dir)
        #
        return output_dir

    @classmethod
    def initializeClass(cls):
        """
        Initializes values of the project ids
        """
        response = requests.get(cn.PROJECT_URL)
        project_descs = response.json()
        cls.PROJECT_DCT = {d["id"]: d for d in project_descs}
        cls.PROJECT_IDS = list(cls.PROJECT_DCT.keys())

    def _copyUrlFile(self, file_url:str, dir_path:str, local_filename:str=None)->str:
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
        if local_filename is None:
            local_filename = util.getFilenameFromUrl(file_url)
        output_path = os.path.join(dir_path, local_filename)
        try:
            with open(output_path, 'wb') as fd:
                fd.write(response.content)
        except Exception as exp:
            import pdb; pdb.set_trace()
            pass
        return output_path

    @classmethod
    def buildContext(cls, context_file_path:str=cn.CONTEXT_FILE, cache_dir:str=cn.CACHE_DIR, report_interval:int=5,
                     first:int=0, last:int=None, sleep_sec:float=0):
        """
        Builds context for all projects. Writes the result to the context file

        Args:
            context_file_path: path for the output csv file
            cache_path: path to where local files are cached
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
        if os.path.isfile(context_file_path):
            context_df = pd.read_csv(context_file_path, index_col=0)
            completed_project_ids = list(context_df.index)
        else:
            completed_project_ids = []
            context_df = pd.DataFrame()
        #
        dct = {k: [] for k in cn.CONTEXT_KEYS}
        generator = cls.iterateProjects(ignored_project_ids=completed_project_ids,
                                         first=first, last=last, report_interval=report_interval)
        for project in generator:
            project.buildProject()
            for key in cn.CONTEXT_KEYS:
                dct[key].append(project.__getattribute__(key))
            #
            project_cache_dir = project.getProjectCacheDirectory(cache_dir=cache_dir)
            if not os.path.isdir(project_cache_dir):
                os.mkdir(project_cache_dir)
            df = pd.DataFrame(dct)
            df = df.set_index(cn.PROJECT_ID)
            df = pd.concat([context_df, df])
            df.to_csv(context_file_path, index=True)
            _ = project._copyUrlFiles()
            project._downloadOutput(cache_dir=cache_dir)  # Download the output files
            project.makeReadableModel(cache_dir=cache_dir)
            if sleep_sec > 0:
                if cn.CHATGPT_HEADER in project.abstract:
                    time.sleep(sleep_sec)
        #
        return df

    def getH5Data(self, is_write:bool=True):
        """
        Recursively searches a Biosimulations HDF5 file for datasets.

        Args:
            is_write: write CSV files for the data 
        
        Returns:
            DataFrame properties
            name (str): name of the dataset
            columns (list-str): variables
        """
        def findDataframes(item, group_names, dfs):
            """
            Recursively searches groups for datasets with sedmlDataSetIds.
            
            Args:
                item: Group/Dataset
                group_names: list-str
                dfs: list-DataFrame
            Returns:
                list-DataFrame
            """
            names = list(group_names)
            if "Dataset" in str(type(item)):
                # Encountered a leaf in the container graph
                if "sedmlDataSetIds" in item.attrs.keys():
                    index = list(item.attrs["sedmlDataSetIds"])
                    if len(item.shape) != 2:
                        print("** Ignored item with strange shape %s" % str(item.shape))
                        return []
                    df = pd.DataFrame(item[:,:], index=index)
                    df = df.T
                    df.name = cn.NAME_SEPARATOR.join(names)
                    dfs.append(df)
                    return dfs
            else:
                new_dfs = []
                for key in item.keys():
                    new_names = list(names)
                    new_names.append(key)
                    this_dfs = findDataframes(item[key], new_names, [])
                    new_dfs.extend(this_dfs)
                result_dfs = list(dfs)
                result_dfs.extend(new_dfs)
                return result_dfs
        #
        h5_path = self.getH5FilePath()
        cache_path = self.getProjectCacheDirectory()
        with h5py.File(h5_path, 'r') as fd:
            dfs = findDataframes(fd, [], [])
        if is_write:
            for df in dfs:
                splits = df.name.split(cn.NAME_SEPARATOR)
                filename = splits[-1] + ".csv"
                path = os.path.join(cache_path, filename)
                df.to_csv(path, index=False)
        return dfs


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
        path_dir = self.getProjectCacheDirectory()
        ffiles = []
        for ffile in os.listdir(path_dir):
            file_path = os.path.join(path_dir, ffile)
            if os.path.isfile(file_path):
                ffiles.append(file_path)
        return ffiles
    
    def makeReadableModel(self, is_write:bool=True, cache_dir:str=None, is_replace:bool=False)->str:
        """
        Converts a model to human readable text, if possible. Currently only
        supports conversion to Antimony. 

        Args:
            is_write: write the model and data to the cache
            is_replace: replace the file if it exiss
            cache_dir: where cached files are

        Returns:
            str: antimony model
        """
        # Get path to the antimony file
        project_cache_dir = self.getProjectCacheDirectory(cache_dir=cache_dir)
        filename = "%s.ant" % self.project_id
        ant_path = os.path.join(project_cache_dir, filename)
        # Handle existing Antimony file
        if (not is_replace) and (os.path.isfile(ant_path)):
            with open(ant_path, "r") as fd:
                lines = fd.readlines()
            model_str = "".join(lines)
        # No existing Antimony file
        else:
            # See if there is an SBML file
            paths = self.getFilePaths()
            sbml_path = None
            for path in paths:
                splits = os.path.splitext(path)
                if (splits[1] == ".xml") and ("manifest" not in path):
                    with open(path, "r") as fd:
                        lines = fd.readlines()
                    model = "\n".join(lines)
                    if not "sbml" in model:
                        continue
                    sbml_path = path
                    break
            # Construct the model string
            model_str = None
            if sbml_path is not None:
                try:
                    rr = te.loadSBMLModel(sbml_path)
                    model_str = rr.getAntimony()
                except:
                    pass
            # Write the file
            if is_write and (model_str is not None):
                
                with open(ant_path, 'w') as fd:
                    fd.writelines(model_str)
        #
        return model_str

    def getH5FilePath(self)->str:
        """
        Provide the path to the HDF5 output file.

        Returns:
            path to file (or None)
        """
        outdir = self.getOutputsDirectory()
        ffiles = [f for f in os.listdir(outdir) if ".h5" in f]
        if len(ffiles) == 0:
            print("*** No output directory for project %" % self.project_id)
            ffile = None
        elif len(ffiles) > 1:
            print ("*** Multile h5 files. Using the first.")
            ffile = ffiles[0]
        else:
            ffile = ffiles[0]
        if ffile is not None:
            return os.path.join(outdir, ffile)
        else:
            return None