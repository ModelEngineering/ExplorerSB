'''Reads data produced by ProjectBuilder'''


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util
from src.ExplorerSB.project_base import ProjectBase

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


class Project(ProjectBase):
    ############################################################################
    # CLASS ATTRIBUTES
    ############################################################################
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

    ############################################################################
    # INSTANCE METHODS
    ############################################################################
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
                    pass

    def _getZipDirPath(self):
        result = os.path.join("local", "cache")
        return os.path.join(result, self.runid)

    def _getZipFilePath(self, filename:str)->str:
        """
        Returns full path
        """
        dir_path = self._getZipDirPath()
        ffile = "%s" % (filename)
        return os.path.join(dir_path, ffile)
    
    def getModelFiles(self)->str:
        """
        Creates a temporary directory with the model files. To obtain the model files from Biosimulations
          1. Get the specification information
          2. Get the model IDs and source from the specification information
          3. Get the experiment location
          4. /specifications{runid}/{experimentLocation}/models/{modelId}
        Returns:
            path to temporary directory with a file for each simulation (modelId.type)
        """
        # FIXME
        return
        # Get the specification inforimation
        url = "%s/specifications/%s" % (cn.API_URL, self.runid)
        _, __, response_nested = util.readBiosimulations(url)
        results = util.indexNested(response_nested, [0, "models"])
        import pdb; pdb.set_trace()
        # Create a temporary directory
        temp_dir = tempfile.TemporaryDirectory()
        # Copy the files to the temporary directory
        for filename in self.getFilenames(cn.MODEL):
            contents = self.getFileContents(filename)
            path = os.path.join(temp_dir.name, filename)
            with open(path, "w") as fd:
                fd.write(contents)

    def getFilenames(self, extension:str)->typing.List[str]:
        """
        Obtains of the names of files in the zip archives.

        Args:
            extension: file extension

        Returns:
            filenames with extension
        """
        zip_file = cn.ZIP_DCT[extension]
        with zipfile.ZipFile(zip_file,'r') as zip:
            ffiles = zip.namelist()
        #
        dir_path = self._getZipDirPath()
        paths = []
        for ffile in ffiles:
            if ffile.startswith(dir_path):
                paths.append(ffile)
        #
        results = [os.path.basename(r) for r in paths]
        return results
    
    def getFileContents(self, filename:str)->str:
        """
        Obtains the contents of a file in the cache for this project.

        Args:
            filename with extension

        Returns:
            str
        """
        path = self._getZipFilePath(filename)
        splits = filename.split(".")
        extension = splits[1]
        if not extension in cn.ZIP_DCT.keys():
            raise RuntimeError("Invalid extension: %s" % extension)
        zip_file = cn.ZIP_DCT[extension]
        with zipfile.ZipFile(zip_file,'r') as zip:
            csv_bytes = zip.read(path)
        #
        return csv_bytes.decode()
    
    def getDefaultFilename(self, extension:str)->str:
        """
        Gets the default filename for the extension

        Args:
            extension (str): file extension

        Returns:
            str: filename
        """
        filename = None
        filenames = self.getFilenames(cn.CSV)
        if len(filenames) > 0:
            for name in filenames:
                if (extension == cn.CSV):
                    if "objective" in name:
                        continue
                filename = name
                break
            #
        return filename
   
    def getCSVData(self, filename:str=None)->pd.DataFrame:
        """
        Obtains the data for the CSV file.

        Args:
            filename with extension

        Returns:
            pd.DataFrame
        """
        if filename is None:
            filename = self.getDefaultFilename(cn.CSV)
        if filename is None:
            return pd.DataFrame()
        csv_str = self.getFileContents(filename)
        csv_sio = StringIO(csv_str)
        df = pd.read_csv(csv_sio, sep=",")
        return df

    def makePlotFigure(self, filename:str=None, title=""):
        """
        Calculates a plotly figure.

        Args:
            filename (str, optional)
        Returns:
            fig (plotly.graph_objs._figure.Figure:)
        """
        df = self.getCSVData(filename=filename)
        # Find the time column, if it exiss
        time_cols = [c for c in df.columns if cn.TIME in c]
        if len(time_cols) == 0:
            return go.Figure()
        else:
            time_col = time_cols[0]
        times = df[time_col]
        # create a list of traces for each column in the dataframe
        traces = []
        for col in df.columns:
            if col != time_col:
                traces.append(go.Scatter(x=times, y=df[col], mode='lines', name=col))
        # create a layout
        title = ""
        if len(traces) == 1:
            columns = [c for c in df.columns if c != time_col]
            if len(columns) == 1:
                title = columns[0]
        layout = go.Layout(title=title, xaxis=dict(title='time'), yaxis=dict(title=title))
        # create a figure
        fig = go.Figure(data=traces, layout=layout)
        return fig

    ############################################################################
    # CLASS METHODS
    ############################################################################
    @classmethod
    def resetClassAttributes(cls):
        cls.PROJECT_IDS = None
        cls.PROJECT_DF = None
        cls.INV_TITLE_DCT = None
        cls.INV_SHORT_TITLE_DCT = None

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
