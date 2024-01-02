"""Creates the data directories."""

import src.ExplorerSB.constants as cn
from src.ExplorerSB.builder import Builder

cn.TRACE_LEVEL = 2 # Give detailed traces. 0 for no trace

import os

builder =  Builder(
                    stage_dir=cn.STAGE_DIR,
                    data_dir=cn.DATA_DIR,
                    is_reset=False)
builder.build()