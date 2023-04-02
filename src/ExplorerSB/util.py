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

def getApikey():
    """
    Gets the API key from a local file.

    Returns
    -------
    str
    """
    with open(cn.APIKEY_FILE, "r") as fd:
        apikey = fd.readline()
    if apikey[-1] == '\n':
        apikey = apikey[:-1]
    return apikey

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

def copyUrlFile(file_url, dir_path):
    """
    Copies the file in the URL to the specifie directory.

    Parameters
    ----------
    file_url: str
    dir_path: str (path to output directory)

    Returns
    -------
    """
    r = requests.get(file_url, allow_redirects=True)
    filename = getFilenameFromUrl(file_url)
    output_path = os.path.join(dir_path, filename)
    with open(output_path, 'wb') as fd:
         fd.write(r.content)
