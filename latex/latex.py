#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LaTeX functions for converting data to LaTeX formats.
"""


def latex_table(df, table_package='tabu', table_width=1, cell_align='c', float_prec=False):
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

    '''
    # SETUP TABLE
    print('%%%%%%%%%%%%%%%%%')
    print('\\begin{table}[htb] % Table')
    print('\\centering')
    # SETUP TABULAR
    ncol = len(df.columns)

    # SETUP the begin tabu or begin tabular line
    line_array = list([''.ljust(4)])
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
    if table_package.lower() == 'tabu':
        print('        \\tabucline[1pt]{-}')
    else:
        print('        \\hline')

    line_array = list([''.ljust(7)])
    for col in df.columns:
        line_array.append(' \\textbf{')
        line_array.append('{}'.format(col))
        line_array.append('} ')
        line_array.append('&')
    del line_array[-1]
    line_array.append('\\\\')
    print(''.join(line_array))
    # PRINT ROWS
    for idx in df.iterrows():
        # PRINT ROWS
        line_array = list(['        \\hline'])
        for col in df.columns:
            value = df[col][idx[0]]
            if float_prec:
                if isinstance(value, (float)):
                    line_array.append(' {:0.{}f}'.format(value, float_prec))
                else:
                    line_array.append(' {0}'.format(value))
            else:
                line_array.append(' {0}'.format(value))
            line_array.append(' &')
        del line_array[-1]
        line_array.append('\\\\')
        print(''.join(line_array))
    if table_package.lower() == 'tabu':
        print('        \\tabucline[1pt]{-}')
        print('    \\end{tabu}')
    else:
        print('        \\hline')
        print('    \\end{tabular}')
    # PRINT END

    print('\\caption[SmallCapt]{LongCaption}')
    print('\\label{tab:tab_key}')
    print('\\end{table}')
    print('%%%%%%%%%%%%%%%%%')
