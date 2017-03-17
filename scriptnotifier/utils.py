#!/usr/bin/env python
# -*- coding: utf-8 -*-
# public
'''utils.py: Contains utility functions for providing status alerts in a script'''
from __future__ import absolute_import, division, print_function
__author__ = 'Warren E. Black'
__date__ = '2015'
__version__ = '1.000'

import textwrap


def printerr(text, width=80, errtype=None):
    """
    Small utility to print custom errors with proper indentation and text wrapping. The only error
    types coded are `error` and `warning`.

    Parameters:
        text (str): String of text without the preceding error flag that will be formated
        width (int): The maximum length of wrapped lines
        errtype (str): Indicate which type of error to format the string as. The default value of
            `None` will only text wrap the string to the specified `width`.

    .. codeauthor:: Warren E. Black - 2015-11-01
    """
    import pygeostat as gs

    if isinstance(errtype, str):
        errtype.lower()
    if errtype is 'error':
        text = 'ERROR: ' + text
        subsequent_indent = "       "
    elif errtype is 'warning':
        text = 'WARNING: ' + text
        subsequent_indent = "         "
    else:
        subsequent_indent = ""
    print(textwrap.fill(text, width=width, subsequent_indent=subsequent_indent))
