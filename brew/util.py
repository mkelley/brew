# Licensed under an MIT style license - see LICENSE

"""
util --- Small utility functions.
=================================

"""

def sg2brix(sg):
    """http://www.brewersfriend.com/brix-converter/"""
    return ((182.461 * sg - 775.6821) * sg + 1262.7794) * sg - 669.5622

def f2c(T):
    """Fahrenheit to Celcius."""
    return (T - 32) * 5 / 9.

def correct_sg(sg, T):
    """Correct specific gravity measurment given temperature (60/60).

    Equation is accurate from 32 F to 212 F.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """
    # T in Fahrenheit
    return sg * (1.00130346
                 - 1.34722124e-4 * T
                 + 2.04052596e-6 * T**2
                 - 2.32820948e-9 * T**3)

def refractometer_fg(sg0, sg_r):
    """Correct final gravity measurment from refractometer.

    sg0 : float
      Starting specific gravity.

    sg_r : float
      Raw (uncorrected) specific gravity measurement from refractometer.
    """
    return 1 - 0.002349 * sg2brix(sg0) + 0.006276 * sg2brix(sg_r)

def sg2plato(sg):
    """Extract in degrees Plato.

    Valid for the range 0 to 33° Plato / 1.000 to 1.144.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """
    return -668.962 + 1262.45 * sg - 776.43 * sg**2 + 182.94 * sg**3

def rows2tab(rows, colnames, footer=None, colformats=None, format='text',
             verbose=True):
    """Format a list of table rows.

    Parameters
    ----------
    rows : list of lists
      Each item is a row of table values.
    colnames : list of strings
      The column names.
    footer : string, optional
      Footer text.
    colformats : list of strings, optional
      Column formats in Python string format mini-language.
    format : string, optional
      'text' (RST), 'html', or 'notebook'.  The latter returns IPython
      notebook objects.
    verbose : bool, optional
      Set to `True` to dipslay the table.

    Returns
    -------
    tab : string or IPython HTML object

    """

    import textwrap

    assert format in ['text', 'html', 'notebook']

    ncols = len(colnames)
    if colformats is None:
        colformats = ['{}'] * ncols

    formatted_tab = []
    for row in rows:
        formatted_row = [f.format(c) for f, c in zip(colformats, row)]
        formatted_tab.append(formatted_row)

    tab = ''

    if format in ['html', 'notebook']:
        thead = '<tr><th>' + '</th><th>'.join(colnames) + '</th></tr>'
        tbody = ['<tr><td>' + '</td><td>'.join(row) + '</td></tr>'
                 for row in formatted_tab]

        tab = """
<table class="table table-condensed table-hover small">
  <thead>
    {thead}
  </thead>""".format(thead=thead)
        if footer is not None:
            tab += """
  <tfoot>
    <tr><td colspan="{ncols}">{tfoot}</td></tr>
  </tfoot>""".format(ncols=ncols, tfoot=footer)

        tab += """
  <tbody>
    {tbody}
  </tbody>
</table>
        """.format(tbody='\n    '.join(tbody))

    else:
        tab += '\n'

        colsize = []
        _rows = [colnames] + formatted_tab
        for cell in range(ncols):
            cell_sizes = [len(row[cell]) for row in _rows]
            colsize.append(max(cell_sizes))

        line = '  '.join(['{{:{}}}'.format(c) for c in colsize])

        # RST borders
        border = line.format(*['=' * c for c in colsize]) + '\n'

        # header
        tab += border
        tab += line.format(*colnames) + '\n'
        tab += border

        # body
        for row in formatted_tab:
            tab += line.format(*row) + '\n'

        # close
        tab += border + '\n'

        if footer is not None:
            tab += footer + '\n'

    if format == 'notebook':
        from IPython.display import HTML, display_html
        tab = HTML(tab)
        if verbose:
            display_html(tab)
    elif verbose:
        print(tab)

    return tab

        
