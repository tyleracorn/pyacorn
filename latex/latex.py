#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LaTeX functions for converting data to LaTeX formats.
"""


def latex_table(df, table_package='tabu', table_width=1, cell_align='c', float_prec=False,
                replace_dict={'_': ' ', '-': ' '}):
    '''A simple function for taking a dataframe and printing out a latex table. Then just Copy and Paste
    into LaTeX!!!!!!

    Parameters:
    df (pandas.DataFrame): Pass it the slice you want.. uses column names for header row
    table_package (str): The table package used. Can be either `tabu' or `tabular'
    table_width (number): Tabue uses a fraction of textwidth. tabular uses width in cm.
    vert_border (str): single ('s') or double ('d') vertical borders around cells
    horz_border (str): single ('s') or double ('d') horizontal borders around cells
    cell_align (str): can be either right ('r'), middle ('m'), left ('l') or centered ('c')
    float_prec(int): If you pass it a int it will evaluate each cell and if it is a float
        it will set the float precision in print out
    replace_dict (dict): A dictionary of string characters to replace so that LaTeX likes the
        output more.

    '''
    # SETUP TABLE
    print('%' * 17)
    print('\\begin{table}[htb] % Table')
    print('\\centering')
    # SETUP TABULAR
    ncol = len(df.columns)

    # SETUP the begin tabu or begin tabular line
    line_array = list([' ' * 4])
    if table_package.lower() == 'tabu':
        line_array.append('\\begin{tabu}')
        line_array.append(' to {width}\\textwidth'.format(width=table_width))
        line_array.append(' { |[1pt]')
    elif table_package.lower() == 'tabular':
        line_array.append('\\begin{tabular}{')
        col_width = table_width / ncol
    else:
        raise ValueError('unsupported table package :', table_package)
    # iterate through the columns
    for x in range(0, ncol):
        if cell_align == 'r':
            line_array.append(' r |'.format(col_width))
        elif cell_align == 'l':
            line_array.append(' l |'.format(col_width))
        elif cell_align == 'c' or cell_align == 'm':
            if table_package.lower() == 'tabu':
                line_array.append(' X[c] |')
            else:
                if cell_align == 'c':
                    line_array.append(' c |')
                else:
                    line_array.append(' m{{{0:.2f}cm}} |'.format(col_width))
    if table_package == 'tabu':
        line_array.append('[1pt] ')
    line_array.append('}')
    print(''.join(line_array))

    # PRINT COLUMN HEADERS
    line_array = list([' ' * 8])
    if table_package.lower() == 'tabu':
        line_array.append('\\tabucline[1pt]{-}')
    else:
        line_array.append('\\hline')
    print(''.join(line_array))

    line_array = list([' ' * 8])
    for col in df.columns:
        line_array.append('\\textbf{')
        # Search column string and replace characters to make LaTeX happy
        column_string = '{}'.format(col)
        for key in replace_dict:
            column_string = column_string.replace(key, replace_dict[key])
        line_array.append(column_string)
        line_array.append('} ')
        line_array.append('&')
    del line_array[-1]
    line_array.append('\\\\')
    print(''.join(line_array))
    # PRINT ROWS
    for idx in df.iterrows():
        # PRINT ROWS
        line_array = list([' ' * 8])
        line_array.append('\\hline')
        for col in df.columns:
            value = df[col][idx[0]]
            if float_prec:
                if isinstance(value, (float)):
                    line_array.append(' {:0.{}f}'.format(value, float_prec))
                elif isinstance(value, (str)):
                    # Search string and replace characters
                    value_string = ' {}'.format(value)
                    for key in replace_dict:
                        value_string = value_string.replace(key, replace_dict[key])
                    line_array.append(value_string)
                else:
                    line_array.append(' {0}'.format(value))
            else:
                if isinstance(value, (str)):
                    # Search string and replace characters
                    value_string = ' {}'.format(value)
                    for key in replace_dict:
                        value_string = value_string.replace(key, replace_dict[key])
                    line_array.append(value_string)
                else:
                    line_array.append(' {0}'.format(value))
            line_array.append(' &')
        del line_array[-1]
        line_array.append('\\\\')
        print(''.join(line_array))

    # PRINT END
    line_array = list([' ' * 8])
    if table_package.lower() == 'tabu':
        line_array.append('\\tabucline[1pt]{-}')
        print(''.join(line_array))
        print('    \\end{tabu}')
    else:
        line_array.append('\\hline')
        print(''.join(line_array))
        print('    \\end{tabular}')

    print('\\caption[SmallCapt]{LongCaption}')
    print('\\label{tab:tab_key}')
    print('\\end{table}')
    print('%' * 17)
