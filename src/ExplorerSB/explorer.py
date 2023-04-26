'''A viewer for information on Biosimulations'''

"""
Limitations
1. Only articles with titles are considered.
"""


import src.ExplorerSB.constants as cn
import src.ExplorerSB.util as util
from src.ExplorerSB.searcher import Searcher
from src.ExplorerSB.project import Project

import dash
from dash import html
import plotly.graph_objs as go
from dash import dcc
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
import json
import pandas as pd
import requests
import yaml
import whoosh.index as index
from whoosh.qparser import QueryParser
from htmldom import htmldom
from requests_html import HTMLSession
import tabulate

# Initialize Project.PROJECT_ID, Project.PROJECT_DF
Project.initializeClass()
######## Constants #######
MAX_TITLE_LENGTH = 100
PROJECT_IDS = [p for p in Project.PROJECT_DF.index if isinstance(Project.PROJECT_DF.loc[p, cn.TITLE], str)]
PROJECT_DF = Project.PROJECT_DF.loc[PROJECT_IDS]
# Eliminate leading and trailing blanks
PROJECT_DF[cn.TITLE] = [t.strip() for t in PROJECT_DF[cn.TITLE]]
PROJECT_TITLES = [t for t in PROJECT_DF[cn.TITLE]]
TITLE_DCT = {title: pid for title, pid in zip(PROJECT_DF[cn.TITLE], PROJECT_DF.index)}
dct = {p: PROJECT_DF.loc[p, cn.TITLE] for p in PROJECT_DF.index}
# key: projectid, value: title
TITLE_DROPDOWN_DCT = {p: t if len(t) <= MAX_TITLE_LENGTH
      else "%s..." % t[:MAX_TITLE_LENGTH] for p, t in dct.items()}
PLACEHOLDER = "placeholder"  # Used if there is no output in a callback
ID_RAD = "project ID"
SEARCHER = Searcher()

# Element identifiers
EID_ABSTRACT = "abstract"
EID_ARTICLE_COUNT = "article-count"
EID_DATA = "data"
EID_DROPDOWN_DATA = "dropdown_data"
EID_DROPDOWN_MODEL = "dropdown_model"
EID_DROPDOWN_TITLE = "dropdown_title"
EID_MODEL = "model"
EID_SEARCH = "search"

# Properties
PRP_CHILDREN = "children"
PRP_VALUE = "value"

# Initializations
project_dropdowns = [dict(label=v, value=v) for v in PROJECT_TITLES]
# Get the indexer
indexer = index.open_dir(cn.INDEX_DIR)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
application = app.server

# UI dfinitions
def makeDropdown(options=project_dropdowns, value=PROJECT_TITLES[0]):
    return dcc.Dropdown(id=EID_DROPDOWN_TITLE, options=options, value=value)
#
dropdown_comp = makeDropdown()
title_col = dbc.Col(dbc.Row([
      html.H2("Selected Titles (%d)" % len(PROJECT_IDS), id=EID_ARTICLE_COUNT,
              style={"padding": "10px 30px"}),
      html.P(children=dropdown_comp, id='dropdown_loc'),
      # Used to handle callbacks without output
      html.P(id=PLACEHOLDER)
      ])
)
space_col = dbc.Col(dbc.Row([
      html.P(" ")
      ])
)
search_col = dbc.Col(dbc.Row([
      dbc.Input(id=EID_SEARCH, placeholder="Enter search terms ...", type="text",
            style={"width": "2000px", "padding": "10px 100px"},
      ),
      ])
)
abstract_col = dbc.Col(dbc.Row([
      html.H2("Research Summary"),
      dcc.Markdown(id = EID_ABSTRACT, style={'whiteSpace': 'pre-line',
            'padding-left': '40px', 'padding-right': '20px', 'background-color': 'Gainsboro'}),
      ])
)
model_col = dbc.Col([
      html.H2("Model", style={"padding": "10px 30px"}),
      dcc.Markdown(
            id = EID_MODEL,
            style={'whiteSpace': 'pre-line',
                  'padding-left': '40px', 'padding-right': '20px', 'background-color': 'Gainsboro', 'margin-right': "1500 px"},
      )
])
data_col = dbc.Col([
      html.H2("Data", style={"padding": "10px 20px"}),
      dcc.Graph(id=EID_DATA),
      #dcc.Markdown( 
      #      id = EID_DATA,
      #      style={'whiteSpace': 'pre-line',
      #            'padding-left': '40px', 'padding-right': '20px', 'background-color': 'Gainsboro'},
       ],
      #style={'whiteSpace': 'pre-line',
      #      'padding-left': '40px', 'padding-right': '20px',
      #      'textAlign': 'center'},
)
download_col = dbc.Col(
      [html.Button('Download', id='download')],
      style={'margin-bottom': '10px',
              'textAlign':'center',
              'width': '220px',
              'margin':'auto'}
)


app.layout = html.Div([
    dbc.Row([
          html.H1("ExplorerSB - Exploring Models in Systems Biology",
                  style={"text-align": "center"}),
          html.Br(),
        ],
        #justify="center", align="center"
    ),
    dbc.Row([
          #space_col,
          search_col, html.Div(style={
            "width": "250px", "padding": "20px"}),
          ],
        justify="center", align="center"
    ),
    dbc.Row([
          title_col,
          abstract_col,
          html.Div(style={"margin-left": "25px"}),
          ],
    ),
    dbc.Row([
          model_col,
          data_col,
          html.Div(style={"margin-left": "25px"}),
          ],
    ),
    dbc.Row([
          download_col,
          ],
    ),
])


######### CALL BACKS ############
#-------- HELPERS -----------#
def calculateAbstractText(project_id, search_result):
    if project_id is None:
        return ""
    #
    project = Project(project_id)
    project.initialize()
    abstract = project.abstract
    # Augment the abstract if there is a search result
    if search_result is not None:
        highlights = search_result.highlights("content")
        highlights = util.removeAngleBrackets(highlights)
        splits = highlights.split("...")
        for split in splits:
            bold_split = "**" + split + "**"
            abstract = project.abstract.replace(split, bold_split)
    # Construct result
    result = "*%s*\n\n%s\n\n%s" % (project.citation, abstract, project.paper_url)
    return result

#-------- CALLBACKS -----------#
@app.callback([Output(component_id=EID_ABSTRACT, component_property= PRP_CHILDREN),
              Output(component_id='dropdown_loc', component_property= PRP_CHILDREN),
              Output(component_id=EID_ARTICLE_COUNT, component_property= PRP_CHILDREN),
              Output(component_id=EID_MODEL, component_property= PRP_CHILDREN),
              #Output(component_id=EID_DATA, component_property= PRP_CHILDREN),
              Output(component_id=EID_DATA, component_property="figure"),
              ],
              [Input(component_id=EID_DROPDOWN_TITLE, component_property= PRP_VALUE),
              Input(component_id=EID_SEARCH, component_property= PRP_VALUE),
              ])
def updateAbstractAndDropdown(selected_title, search_text):
    """
    Inputs have the follow effects on outputs:
    selected_title: updates the abstract
    search: selects a subset of options for dropdown
    """
    # Find the project id associated with the title
    if selected_title is None:
        import pdb; pdb.set_trace()
    title = selected_title
    max_len = MAX_TITLE_LENGTH - len("...")
    if len(title) > max_len:
        title = selected_title[:max_len]
    dropdown_pids = [p for p, t in TITLE_DROPDOWN_DCT.items()
                    if t[:max_len] == title]
    for pid, title in TITLE_DROPDOWN_DCT.items():
        if title[:MAX_TITLE_LENGTH] == selected_title[:MAX_TITLE_LENGTH]:
            dropdown_pids.append(pid)
    if len(dropdown_pids) > 0:
        selected_pid = dropdown_pids[0]
    else:
        selected_pid = None
    # Calculate the subset of project_ids based on search_text
    search_results = None
    search_result = None
    permitted_ids = list(PROJECT_IDS)
    if (search_text is None) or (len(search_text) < 3):
        search_result_dct = None
    else:
        _, search_results = SEARCHER.search(search_text + "*")
        search_result_dct = {r['title']: r['content'] for r in search_results}
        permitted_ids = list(set(permitted_ids).intersection(search_result_dct.keys()))
    # Construct the dropdown options
    dropdown_options = [TITLE_DROPDOWN_DCT[p] for p in permitted_ids]
    # Construct the new selected project
    if selected_pid in permitted_ids:
        new_selected_pid = selected_pid
    else:
        if len(permitted_ids) > 0:
            new_selected_pid = permitted_ids[0]
        else:
            new_selected_pid = None
    if new_selected_pid is not None:
        project = Project(new_selected_pid)
        project.initialize()
    else:
        project = None
    # Construct the dropdown options
    dropdown_options = [t for p, t in TITLE_DROPDOWN_DCT.items() if p in permitted_ids]
    # Construct the selected options
    if project is not None:
        new_selected_option = TITLE_DROPDOWN_DCT[new_selected_pid]
        # Get the model
        model_filenames = project.getFilenames(cn.ANT)
        model_filenames.extend(project.getFilenames(cn.CELLML))
        model_filenames.extend(project.getFilenames(cn.XML))
        model_filenames.extend(project.getFilenames(cn.SEDML))
        if len(model_filenames) > 0:
            model_filename = model_filenames[0]
            model_str = "``" + project.getFileContents(model_filename) + "``"
            data_str = project.getDefaultCSVData().to_markdown()
        else:
            model_filename = None
            model_str = ""
            data_str = ""
    else:
        new_selected_option = ""
        model_str = ""
    # Find the search result for the selected project
    if (new_selected_pid is not None) and (search_result_dct is not None):
        for result in search_results:
            if result['title'] == selected_pid:
                search_result = result
                break
    # Calculate the final values
    abstract = calculateAbstractText(new_selected_pid, search_result)
    dropdown_comp = makeDropdown(options=dropdown_options, value=new_selected_option)
    fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
    article_count = "%d Titles" % len(permitted_ids)
    return abstract, dropdown_comp, article_count, model_str, fig


if __name__ == '__main__':
    app.run_server(debug=True)
