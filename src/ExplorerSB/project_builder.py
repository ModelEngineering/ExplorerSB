'''Builds a single project. Constructs context data. Downloads files into staging area. Copies selected files to data directory.'''

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

Notes
  1. Does not keep any .json file
"""


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util
from src.ExplorerSB.summary_parser import BiosimulationsSummaryParser
from src.ExplorerSB.project_base import ProjectBase

import h5py
import os
import pandas as pd
import shutil
import tellurium as te
import typing
import zipfile


class ProjectBuilder(ProjectBase):

    def __init__(self, project_id: str, runid: str, data_dir:str=cn.DATA_DIR, stage_dir:str=cn.STAGING_DIR):
        """
        Creates the context entry for a project.

        Args:
            project_id: unique identifier for a project
            data_dir: directory in which project context is stored
        """
        super().__init__(project_id, data_dir=data_dir)
        self.stage_dir = stage_dir
        self.runid = runid
    
    def buildProject(self):
        """
        Constructs the context entry for a project

        Returns:
            dict: key, value for each context entry
        """
        summary_parser = BiosimulationsSummaryParser(self.project_id)
        summary_parser.do()
        # Create the context information
        self.abstract = summary_parser.abstract
        self.citation = summary_parser.citation
        self.title = summary_parser.title
        self.doi = summary_parser.doi
        self.paper_url = summary_parser.paper_url
        # Construct and populate the staging directory
        _ = self._makeStagingData()  # Download the output files
        _ = self._makeCSVFiles()  # Create CSV files from the HDF5 files
        self._makeReadableModel()
        # Create the output data
        self._makeOutputData()

    def _makeOutputData(self):
        """
        Creates the output data directory once the project has been staged.
        """
        data_dir = self.getProjectDir(self.data_dir)
        if os.path.isdir(data_dir):
            shutil.rmtree(data_dir)
        shutil.copytree(self.getProjectDir(self.stage_dir), data_dir)
        # Remove the JSON files
        self._removeJsonFiles(data_dir)

    def _makeStagingData(self)->typing.List[str]:
        """
        Copies the files to the staging directory, creates CSV files from HDF5, and creates Antimony models.

        Returns:
            list of paths copied
        """
        copied_paths = []
        project_dir = self.getProjectDir(is_create=True,
                                                          dest_dir=self.stage_dir)
        file_urls = self._getUrlFileList()
        for file_url in file_urls:
            path = self._copyUrlFile(file_url, project_dir)
            if path.endswith(cn.JSON):
                continue
            if path is not None:
                copied_paths.append(path)
        return copied_paths
    
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
        project_cache_dir = self.getProjectDir()
        _ = self._copyUrlFile(url, project_cache_dir, local_filename=LOCAL_FILENAME)
        zip_path = os.path.join(project_cache_dir, LOCAL_FILENAME)
        # Unzip the file
        output_dir = self.getProjectDir(self.stage_dir, is_create=True)
        if os.path.isdir(output_dir):
            shutil.rmtree(output_dir)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(project_cache_dir)
        self._removeJsonFiles(output_dir)
        #
        return output_dir
    
    @staticmethod 
    def _removeJsonFiles(directory:str):
        """
        Removes JSON files from the directory

        Args:
            directory: directory to clean
        """
        ffiles = [f for f in os.listdir(directory) if f.endswith(cn.JSON)]
        for ffile in ffiles:
            os.remove(os.path.join(directory, ffile))

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
        with open(output_path, 'wb') as fd:
            fd.write(response.content)
        return output_path

    def _makeCSVFiles(self, is_write:bool=True):
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
                if "sedmlDataSetLabels" in item.attrs.keys():
                    index = list(item.attrs["sedmlDataSetLabels"])
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
        h5_path = self._getH5FilePath()
        cache_path = self.getProjectDir()
        with h5py.File(h5_path, 'r') as fd:
            dfs = findDataframes(fd, [], [])
        if is_write:
            for df in dfs:
                splits = df.name.split(cn.NAME_SEPARATOR)
                filename = splits[-1] + ".csv"
                path = os.path.join(cache_path, filename)
                df.to_csv(path, index=False)
        return dfs
    
    def _getH5FilePath(self)->str:
        """
        Provide the path to the HDF5 output file.

        Returns:
            path to file (or None)
        """
        outdir = self.getProjectDir(self.stage_dir)
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
    
    def _makeReadableModel(self, is_write:bool=True, is_replace:bool=False)->str:
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
        project_cache_dir = self.getProjectDir()
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