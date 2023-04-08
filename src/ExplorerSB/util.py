import src.ExplorerSB.constants as cn

import copy
import os
import pandas as pd
import requests


def cleanDF(df):
    """
    Removes suprious columns from a DataFrame.

    Parameters
    ----------
    df: DataFrame

    Returns
    -------
    DataFrame
    """
    new_df = df.copy()
    names = ["Unnamed", "level_", "index"]
    for column in new_df.columns:
        for name in names:
            if name in column:
                del new_df[column]
    return new_df

def indexNested(struct, keys, default=None):
        """
        Reliably indexes a nested structure of lists and dictionaries.

        Parameters
        ----------
        struct: nested structure of dictionaries, lists
        keys: list of indices/keys
        default: value to return if index fails

        Returns
        -------
        object
        """
        cur_struct = copy.deepcopy(struct)
        for key in keys:
            try:
                cur_struct = cur_struct[key]
            except (TypeError, KeyError, IndexError):
                return default
        #
        return cur_struct

def setValue(value, default):
    if value is None:
        return default
    return value

def removeAngleBrackets(text):
        """
        Removes angle bracket sequences, such as in HTML, XML. For
        example:
            hello <b class=x other=y>this is text</b> goodby
        becomes
            hello this is text goodby
        Cannot handle nested brackets.

        Parameters
        ----------
        text: str

        Returns
        -------
        str
        """
        LEFT_BRACKET = "<"
        RIGHT_BRACKET = ">"
        #
        split_text = text.split(RIGHT_BRACKET)
        new_text = ""
        for segment in split_text:
            pos = segment.find(LEFT_BRACKET)
            if pos >= 0:
                new_text += segment[:pos]
        #
        return new_text


def getFilenameFromUrl(file_url):
    """
    Extracts the file name from the URL.

    Parameters
    ----------
    file_url: str

    Returns
    -------
    str
    """
    splits = file_url.split("/")
    return splits[-1]

def readBiosimulations(url:str, **kwargs):
    """
    Issues REST command to api.biosimulations.org

    Args:
        url (str):
        kwargs: keyword arguments passed to requests.get
    Returns:
        requests.models.Response
        str
        nested (dict, list, None): json interpreted as a python structure
    """
    response = requests.get(url, **kwargs)
    response_str = response.content.decode()
    null = None
    false = False
    true = True
    try:
        response_nst = eval(response_str)
    except:
        response_nst = None # Could not interpret the structure
    return response, response_str, response_nst