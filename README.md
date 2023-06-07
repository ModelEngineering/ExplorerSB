# EXPLORERSB - EXPLORING QUANTITATIVE MODELS IN SYSTEMS BIOLOGY

# Overview
This project is about providing a self-descring dash board for researchers interested in quantitative models in systems biology.
The source of the models is the [Biosimulations](http://biosimulations.org) project. This project provides an extensive set of web
pages that describes prodictions produced by quantitative models, the quantiative models,  and the research papers that describe
these data and models. Although a great deal of detail can be obtained from this dashboard, using it requires some training.

ExplorerSB is intended for system biology researchers who are more casual users of the information in Biosimulations.
To this end, ExplorerSB provides a simple user interface to:

* *find* articles relevant to a researchers area of interest;
* *view* the model developed in these articles; and
* *explore* the data produced by the models.

# Architecture
ExplorerSB is structured as two applications: an off-line application and an on-line (user interacting) application.
The off-line application builds local files with information from Biosimulations that
is used in the on-line application. This information includes: information about the published article (e.g., title, full citation, abstract),
the quantiative model (e.g., SBML), and data produced from the model (as CSV files).
The on-line application uses this information to allow users to find articles, view models, and explore model predictions.

## Off-line application
* ``builder.py`` controls the overall workflow. It makes use of a staging directory where files are downloaded and
a data directory that is zipped.
*  ``project_builder.py`` builds a single project
*  ``project_base.py`` provides common codes for the on-line and off-line applications
*  ``summary_parser.py`` parses the summary JSON provided by BioSimulations.

# Data
Data created by the off-line application are in the ``data`` folder. The zip files have the directory structure ``local/cache/<runid>``.