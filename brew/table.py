# Licensed under an MIT style license - see LICENSE

"""
table --- Simple class for tablular data.
=========================================

"""

__all__ = [
    'Table',
]


class Table:
    """Tabular data formatter.

    Parameters
    ----------
    data : array of arrays
      The data as columns.
    names : array of strings
      The names of each column.
    caption : string, optional
      Table caption for yaml format.
    format : string, optional
      The table format for string output: text, html, notebook, or yaml.

    Attributes
    ----------
    colformat : array of strings
      Formats for the values in each column.
    footer : string
      The table footer.

    """

    def __init__(self, data=None, names=None, caption=None, format='text'):
        self.data = data
        self.names = list(names)
        self.caption = caption
        self._colformats = None
        self.footer = ''
        assert format in ['text', 'html', 'notebook', 'yaml']
        self.format = format

    @property
    def colformats(self):
        if self._colformats is None:
            return ['{}'] * len(self.data)
        else:
            return self._colformats

    @colformats.setter
    def colformats(self, f):
        self._colformats = f

    def __str__(self):
        from collections import OrderedDict
        ncols = len(self.data)

        formatted_tab = []
        for row in zip(*self.data):
            formatted_row = [f.format(c) for f, c in zip(self.colformats, row)]
            formatted_tab.append(formatted_row)

        tab = ''
        if self.format in ['html', 'notebook']:
            thead = '<tr><th>' + '</th><th>'.join(self.names) + '</th></tr>'
            tbody = ['<tr><td>' + '</td><td>'.join(row) + '</td></tr>'
                     for row in formatted_tab]

            tab = """
<table class="table table-condensed table-hover small">
  <thead>
    {thead}
  </thead>""".format(thead=thead)
            if self.footer is not None:
                tab += """
  <tfoot>
    <tr><td colspan="{ncols}">{tfoot}</td></tr>
  </tfoot>""".format(ncols=ncols, tfoot=self.footer.replace('\n', '<br/>'))

            tab += """
  <tbody>
    {tbody}
  </tbody>
</table>
""".format(tbody='\n    '.join(tbody))

        elif self.format == 'yaml':
            import textwrap
            import yaml

            tab = {}
            tab['type'] = 'table'
            tab['caption'] = self.caption
            tab['headings'] = self.names
            tab['footer'] = {}
            tab['footer']['rows'] = []
            for row in self.footer.splitlines():
                tab['footer']['rows'].append([{
                    'data': row,
                    'colspan': len(self.names)
                }])
            tab['rows'] = formatted_tab

            # hardcoded indent for my brewlog
            tab = textwrap.indent(yaml.dump([tab]), ' ' * 6)
        else:
            colsize = []
            _rows = [self.names] + formatted_tab
            for cell in range(ncols):
                cell_sizes = [len(row[cell]) for row in _rows]
                colsize.append(max(cell_sizes))

            line = '  '.join(['{{:{}}}'.format(c) for c in colsize])

            # RST borders
            border = line.format(*['=' * c for c in colsize]) + '\n'

            # header
            tab += border
            tab += line.format(*self.names) + '\n'
            tab += border

            # body
            for row in formatted_tab:
                tab += line.format(*row) + '\n'

            # close
            tab += border + '\n'

            if self.footer is not None:
                tab += self.footer + '\n'

        if self.format == 'notebook':
            from IPython.display import HTML, display_html
            tab = HTML(tab)

        return tab
