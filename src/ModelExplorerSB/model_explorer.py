'''A viewer for information on Biosimulations'''
"""
TO DO
1. Highlights are picking up title, not abstract.
"""


import src.ModelExplorerSB.constants as cn
import src.ModelExplorerSB.util as util
from src.ModelExplorerSB.searcher import Searcher

import dash
from dash import html
import plotly.graph_objects as go
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

"""
Get the fiels in a run
https://api.biosimulations.org/files/<runid>
# Model for the runid
https://storage.googleapis.com/files.biosimulations.org/simulations/61fea483f499ccf25faafc4d/contents/model.xml
# Simulation results
https://storage.googleapis.com/files.biosimulations.org/simulations/61fea483f499ccf25faafc4d/contents/expected-results.json
# Simulation data
https://storage.googleapis.com/files.biosimulations.org/simulations/61fea483f499ccf25faafc4d/contents/reports.h5
"""

######## Constants #######
ABSTRACT_DF = pd.read_csv(cn.ABSTRACT_FILE)
ABSTRACT_DF.index = ABSTRACT_DF[cn.ID]
ABSTRACT_DF = util.cleanDF(ABSTRACT_DF)
MAX_TITLE_LENGTH = 100
API_URL = "https://api.biosimulations.org"
CHILDREN = 'children'
PROJECT_URL = "%s/projects" % API_URL
response = requests.get(PROJECT_URL)
project_descs = response.json()
PROJECT_DCT = {d["id"]: d for d in project_descs}
PROJECT_IDS = list(PROJECT_DCT.keys())
# The value is the abstract
PROJECT_DCT = {n: n if not n in ABSTRACT_DF.index
      else ABSTRACT_DF.loc[n, cn.TITLE] for n in PROJECT_IDS}
PROJECT_DCT = {n: n if str(PROJECT_DCT[n]) == 'nan' else PROJECT_DCT[n]
      for n in PROJECT_DCT.keys()}
PROJECT_TITLES = list(PROJECT_DCT.values())
INVERSE_PROJECT_DCT = {v: k for k, v in PROJECT_DCT.items()}
TITLE_DROPDOWN_DCT = {d: d if len(d) <= MAX_TITLE_LENGTH
      else "%s..." % d[:MAX_TITLE_LENGTH] for d in PROJECT_TITLES}
TITLE_DROPDOWNS = list(TITLE_DROPDOWN_DCT.values())
INVERSE_TITLE_DROPDOWN_DCT = {v: k for k, v in TITLE_DROPDOWN_DCT.items()}
PAPER_URL = "https://www.google.com/search?q=Mathematical%20modeling%20of%20heat%20shock%20protein%20synthesis%20in%20response%20to%20temperature%20change"
PLACEHOLDER = "placeholder"  # Used if there is no output in a callback
TITLE_RAD = "title"
ID_RAD = "project ID"
SEARCHER = Searcher()

####### State Object ########
class OptionState():

    def __init__(self, radio_button=ID_RAD, project_id=PROJECT_IDS[0]):
        self.radio_button = radio_button
        self.project_id = project_id
OPTION_STATE = OptionState()

# Initializations
project_dropdowns = [dict(label=v, value=v) for v in PROJECT_IDS]
# Get the indexer
indexer = index.open_dir(cn.INDEX_DIR)

#summary_url = "%s/projects/%s/summary" % (API_URL, PROJECT_IDS[0])
#response = requests.get(summary_url)
#print(yaml.dump(json.loads(response.content), default_flow_style=False))

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
application = app.server

# UI dfinitions
def makeDropdown(options=project_dropdowns, value=PROJECT_IDS[0]):
    return dcc.Dropdown(id='dropdown1', options=options, value=value)
#
dropdown_comp = makeDropdown()
project_col = dbc.Col(dbc.Row([
      dcc.RadioItems(id = 'input-radio-button',
            options = [
                  dict(label = TITLE_RAD, value = TITLE_RAD),
                  dict(label = ID_RAD, value = ID_RAD),
            ],
            value=ID_RAD,
            labelStyle={'display': 'block'}
      ),
      html.H2("Select (%d)" % len(PROJECT_IDS), id='article_count'),
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
      dbc.Input(id="search", placeholder="Enter search terms ...", type="text",
            style={'textalign': 'center'},
      ),
      ])
)
abstract_col = dbc.Col(dbc.Row([
      html.H2("Research Summary"),
      dcc.Markdown(id = 'Abstract', style={'whiteSpace': 'pre-line',
            'padding-left': '40px', 'padding-right': '20px'}),
      ])
)
details_col = dbc.Col(dbc.Row([
      html.H2("Details"),
      dcc.Markdown(id = 'Details', style={'whiteSpace': 'pre-line',
            'padding-left': '40px'})
      ])
)
model_summary_col = dbc.Col([
      html.H2("Model Elements"),
      dcc.Markdown( 'Glu: [Glucose](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:17234)',
            id = 'Model Summary',
            style={'whiteSpace': 'pre-line',
                  'padding-left': '40px', 'padding-right': '20px'},
      )
])
model_details_col = dbc.Col([
      html.H2("Model Details"),
      dcc.Markdown( 'A + B -> C',
            id = 'Model Details',
            ),
      ],
      style={'whiteSpace': 'pre-line',
            'padding-left': '40px', 'padding-right': '20px',
            'textAlign': 'center'},
)
simulation_col = dbc.Col([
      html.H2("Simulation"),
      dcc.Markdown( 'A Graph',
            id = 'Simulation',
      ) ],
      style={'whiteSpace': 'pre-line',
            'padding-left': '40px', 'padding-right': '20px',
            'textAlign': 'center'},
)
download_col = dbc.Col(
      [html.Button('Download', id='download')],
      style={'margin-bottom': '10px',
              'textAlign':'center',
              'width': '220px',
              'margin':'auto'}
)



#@app.callback(Output('output-text', CHILDREN),
#              [Input('input-radio-button', 'value')])
#def update_graph(value):
#    return f'The selected value is {value}'


app.layout = html.Div([
    dbc.Row([
          html.H1("Query BioSimulations"),
          html.Br(),
        ],
        justify="center", align="center"
    ),
    dbc.Row([
          space_col,
          search_col, html.Div(style={"margin-left": "25px"}),
          space_col,
          ]
    ),
    dbc.Row([
          project_col,
          abstract_col,
          html.Div(style={"margin-left": "25px"}),
          ],
    ),
    dbc.Row([
          details_col,
          ],
    ),
    dbc.Row([
          model_summary_col,
          model_details_col,
          simulation_col,
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
def calculateAbstractText(project_id, search_result=None):
    summary_url = "%s/projects/%s/summary" % (API_URL, project_id)
    response = requests.get(summary_url)
    null = None
    dct = eval(response.content.decode())
    # URI
    uri = util.setValue(util.indexNested(dct,
          ["simulationRun", "metadata", 0, "citations", 0, "uri"]),
          "No URI found.")
    # Abstract and citation
    if project_id in ABSTRACT_DF.index:
        # FIXME: search_result does not match the project_id
        abstract = ABSTRACT_DF.loc[project_id, "abstract"]
        if search_result is not None:
            highlights = search_result.highlights("content")
            highlights = util.removeAngleBrackets(highlights)
            splits = highlights.split("...")
            for split in splits:
                bold_split = "**" + split + "**"
                abstract = abstract.replace(split, bold_split)
        citation = ABSTRACT_DF.loc[project_id, "citation"]
        if not isinstance(abstract, str):
            abstract = abstract.values[0]
        if not isinstance(citation, str):
            citation = citation.values[0]
    else:
        citation = "No citation found. "
        abstract = util.setValue(util.indexNested(dct,
              ["simulationRun", "metadata", 0, "abstract"]), "No abstract found.")
    # Construct result
    citation = "*" + citation + "*"
    result = "%s\n\n%s\n\n%s" % (citation, abstract, uri)
    return result

#-------- CALLBACKS -----------#
@app.callback([Output(component_id='Abstract', component_property= CHILDREN),
              Output(component_id='dropdown_loc', component_property= 'children'),
              Output(component_id='article_count', component_property= 'children'),
              ],
              [Input(component_id='dropdown1', component_property= 'value'),
              Input(component_id='input-radio-button', component_property= 'value'),
              Input(component_id='search', component_property= 'value'),
              ])
def updateAbstractAndDropdown(dropdown1_value, radio_value, search_text):
    """
    Inputs have the follow effects on outputs:
       dropdown1_value (dropdown1_value): updates the abstract
       input-radio-button: Determines the options for dropdown
       search: selects a subset of options for dropdown
    """
    # Calculate the subset of project_ids based on search_text
    if (search_text is None) or (len(search_text) < 3):
        permitted_ids = list(PROJECT_IDS)
        search_result_dct = None
    else:
        permitted_ids, search_results = list(SEARCHER.search(search_text + "*"))
        search_result_dct = {p: r for p, r in zip(permitted_ids, search_results)}
    # Classify the current set of dropdown options and find project_id
    if dropdown1_value in PROJECT_IDS:
        # Dropdown has project IDs
        is_projectid_option = True
        project_id = dropdown1_value
    else:
        # Dropdown has project titles
        is_projectid_option = False
        if len(dropdown1_value) == 0:
            project_id = PROJECT_IDS[0]
        else:
            # Extract the project ID from the title
            if dropdown1_value in INVERSE_TITLE_DROPDOWN_DCT.keys():
                full_title = INVERSE_TITLE_DROPDOWN_DCT[dropdown1_value]
                project_id = INVERSE_PROJECT_DCT[full_title]
            elif dropdown1_value in INVERSE_TITLE_DROPDOWN_DCT.keys():
                project_id = INVERSE_PROJECT_DCT[dropdown1_value]
            else:
                # Can't find this ID. Use the first permitted one.
                project_id = PROJECT_IDS[0]
    # Handle project_id not in the permitted list
    if not project_id in permitted_ids:
        if len(permitted_ids) > 0:
            project_id = permitted_ids[0]
        else:
            project_id = None
    # Construct the search result
    if (search_result_dct is None) or (project_id is None):
        search_result = None
    else:
        search_result = search_result_dct[project_id]
    # Calculate the dropdown options
    if radio_value == TITLE_RAD:
        permitted_titles = [PROJECT_DCT[p] for p in permitted_ids]
        dropdown_options = [TITLE_DROPDOWN_DCT[t] for t in permitted_titles]
        if project_id is not None:
            new_dropdown1_value = PROJECT_DCT[project_id]
        else:
            new_dropdown1_value = ""
    else:
        dropdown_options = permitted_ids
        if project_id is not None:
            new_dropdown1_value = project_id
        else:
            new_dropdown1_value = ""
    # Generate the return values
    abstract = calculateAbstractText(project_id, search_result=search_result)
    dropdown_comp = makeDropdown(options=dropdown_options, value=new_dropdown1_value)
    article_count = "Select (%d)" % len(permitted_ids)
    return abstract, dropdown_comp, article_count

@app.callback(Output(component_id='Details', component_property= CHILDREN),
              [Input(component_id='dropdown1', component_property= 'value')])
def getProjectDetails(project_id):
    summary_url = "%s/projects/%s/summary" % (API_URL, project_id)
    response = requests.get(summary_url)
    null = None
    dct = eval(response.content.decode())
    result = str(yaml.dump(json.loads(response.content), default_flow_style=False))
    return result

#@app.callback(Output(component_id='dropdown1', component_property= 'options'),
#              [Input(component_id='search', component_property= 'value')])
#def getSearchTerms(term):
#    return project_dropdowns
#    if len(term) > 0:
#        with indexer.searcher() as searcher:
#            new_term = term + "*"
#            query = QueryParser("content", indexer.schema).parse(new_term)
#            query_result = searcher.search(query)
#            query_ids = [PROJECT_IDS[p[0]] for p in query_result.items()]
#            query_dropdowns = [dict(label=v, value=v) for v in query_ids]
#            import pdb; pdb.set_trace()
#            print(query_dropdowns)
#            return query_dropdowns
#    else:
#        return project_dropdowns

## Handle change in type of abstract display
#@app.callback(Output(component_id='Abstract', component_property= CHILDREN, allow_duplicate=True),
#              [Input('input-radio-button', 'value')])
#def updateAbstractMode(value):
#    OPTION_STATE.radio_button = value
#    text = calculateAbstractText(OPTION_STATE.project_id)
#    return text



if __name__ == '__main__':
    app.run_server(debug=True)
