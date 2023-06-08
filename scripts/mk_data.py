"""Creates the data directories."""

import src.ExplorerSB.constants as cn
from src.ExplorerSB.builder import Builder

import os

builder =  Builder(
                                #project_specification_csv=cn.PROJECTS_CSV,
                                stage_dir=cn.STAGE_DIR,
                                data_dir=cn.DATA_DIR,
                                context_path=cn.CONTEXT_FILE, is_reset=True)
builder.build()
