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

def sg2plato(sg):
    """Extract in degrees Plato.

    Valid for the range 0 to 33° Plato / 1.000 to 1.144.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """
    return -668.962 + 1262.45 * sg - 776.43 * sg**2 + 182.94 * sg**3

def tab2txt(tab, colnames, footer, colformats=None, html=False):
    """Format a list of table rows as text.

    Parameters
    ----------
    tab : list of lists
      Each item is a row of table values.
    colnames : list of strings
      The column names.
    footer : string
      Footer text.
    colformats : list of strings, optional
      Column formats in Python string format mini-language.
    html : bool, optional
      True to return an HTML-formatted table.

    """

    ncols = len(colnames)
    if colformats is None:
        colformats = ['{}'] * ncols

    formatted_tab = []
    for row in tab:
        formatted_row = [f.format(c) for f, c in zip(colformats, row)]
        formatted_tab.append(formatted_row)

    outs = ''

    if html:
        thead = '<tr><th>' + '</th><th>'.join(colnames) + '</th></tr>'
        rows = ['<tr><td>' + '</td><td>'.join(row) + '</td></tr>'
                for row in formatted_tab]

        outs = """
<table class="table table-condensed table-hover">
  <thead>
    {thead}
  </thead>
  <tfoot>
    <tr><td colspan="{ncols}">{tfoot}</td></tr>
  </tfoot>
  <tbody>
    {tbody}
  </tbody>
</table>
        """.format(thead=thead, ncols=ncols, tfoot=footer,
                   tbody='\n    '.join(rows))
    else:
        colsize = []
        for i in range(ncols):
            rows = [colnames] + formatted_tab
            cell_sizes = [len(row[i]) for row in rows]
            colsize.append(max(cell_sizes))

        line = ''
        for c in colsize:
            line += '{{:{}}}  '.format(c)

        outs += '\n'
        for row in [colnames] + [['-' * c for c in colsize]] + formatted_tab:
            outs += line.format(*row) + '\n'

        outs += '-' * (sum(colsize) + (ncols - 1) * 2) + '\n'
        outs += footer + '\n'

    return outs

        
