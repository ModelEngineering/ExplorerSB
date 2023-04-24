'''Builds context data used for the Project class'''

"""
Project context:
    Abstract
    Citation
    DOI
    PROJECT_ID (key)
    RUNID
    TITLE
    PAPER_URL

Conventions:
    In general, the key for a dictionary is the project_id.
    Dictionaries with an "inv" prefix, have a value of project_id.
"""


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util
from src.ExplorerSB.summary_parser import SummaryParser
from src.ExplorerSB.project_base import ProjectBase

import h5py
import os
import pandas as pd
import requests
import shutil
import tellurium as te
import time
import typing
import zipfile

MAX_TITLE_LENGTH = 100


class ProjectBuilder(ProjectBase):

    # Class attributes
    PROJECT_DCT = None
    PROJECT_IDS = None  # List of project IDs

    def __init__(self, project_id: str, data_dir:str=cn.DATA_DIR):
        """
        Creates the context entry for a project.

        Args:
            project_id: unique identifier for a project
            data_dir: directory in which project context is stored
        """
        super().__init__(project_id, data_dir=data_dir)
    
    @classmethod
    def initializeClass(cls):
        """
        Initializes values of the project ids
        """
        response = requests.get(cn.PROJECT_URL)
        project_descs = response.json()
        cls.PROJECT_DCT = {d["id"]: d for d in project_descs}
        cls.PROJECT_IDS = list(cls.PROJECT_DCT.keys())

    def getOutputsDirectory(self):
        project_cache_dir = self.getProjectCacheDirectory()
        return os.path.join(project_cache_dir, "outputs")

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
        # Get the files for the project
        _ = self._copyUrlFiles()  # Download the output files
        self.makeReadableModel()

    def _copyUrlFiles(self)->typing.List[str]:
        """
        Copies the files to the Cache

        Args:
            cache_dir: path to the parent directory destination directory

        Returns:
            list of paths copied
        """
        copied_paths = []
        project_cache_dir = self.getProjectCacheDirectory(is_create=True)
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
    
    def _downloadOutput(self)->str:
        """
        Downloads the output file and unzips it.

        Returns:
            path to the directory
        """
        LOCAL_FILENAME = "output.zip"
        url = "%s/results/%s/download" % (cn.API_URL, self.runid)
        project_cache_dir = self.getProjectCacheDirectory()
        _ = self._copyUrlFile(url, project_cache_dir, local_filename=LOCAL_FILENAME)
        zip_path = os.path.join(project_cache_dir, LOCAL_FILENAME)
        # Unzip the file
        output_dir = self.getOutputsDirectory()
        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(project_cache_dir)
        #
        return output_dir

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
    def buildContext(cls, context_file_path:str=cn.CONTEXT_FILE, data_dir:str=cn.CACHE_DIR, report_interval:int=5,
                     first:int=0, last:int=None, sleep_sec:float=2):
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
        for idx, pid in enumerate(cls.PROJECT_IDS):
            if (idx < first) or (idx > last):
                continue
            if pid in completed_project_ids:
                continue
            builder = ProjectBuilder(pid, data_dir=data_dir)
            builder.buildProject()
            for key in cn.CONTEXT_KEYS:
                dct[key].append(builder.__getattribute__(key))
            # Add to the output DataFrame
            df = pd.DataFrame(dct)
            df = df.set_index(cn.PROJECT_ID)
            df = pd.concat([context_df, df])
            df.to_csv(context_file_path, index=True)
            completed_project_ids.append(pid)
            # Report if required
            if idx % report_interval == 0:
                print("** Processed %d projects." % (idx + 1))
            # Don't go too fast for ChatGPT
            if sleep_sec > 0:
                if cn.CHATGPT_HEADER in builder.abstract:
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
    
    def makeReadableModel(self, is_write:bool=True, is_replace:bool=False)->str:
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
        project_cache_dir = self.getProjectCacheDirectory()
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