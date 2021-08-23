![CircleCI](https://img.shields.io/circleci/build/gh/schireson/htmxl/master) [![Coverage
Status](https://coveralls.io/repos/github/schireson/htmxl/badge.svg?branch=master)](https://coveralls.io/github/schireson/htmxl?branch=master)
[![Documentation](https://readthedocs.org/projects/htmxl/badge/?version=latest)](https://htmxl.readthedocs.io/en/latest/?badge=latest)

## Introduction

``` python
from htmxl.compose import Workbook

workbook = Workbook()
workbook.add_sheet_from_template(
    template="""
    <head>{{ title }}</head>
    <body>
      <div>
        Hello down there, {{ name }}!
      </div>
      <div>
        <table>
          <thead>
            <tr>
              {% for column_name in column_names %}
                <th>{{ column_name }}</th>
              {% endfor %}
            </tr>
          </thead>
          <tbody>
            {% for row in rows %}
              <tr>
                <td>{{ row.a }}</td>
                <td>{{ row.b }}</td>
              </tr>
            {% endfor %}
          </tbody>
        </table
      </div>
    </body>
    """,
    data=dict(
        title="Hello World",
        name='Bob',
        column_names=['A', 'B'],
        rows=[{'a': 'a', 'b': 2}, {'a': 'b', 'b': 2}, {'a': 'c', 'b': 3}],
    )
)

workbook.compose('hello_world.xlsx')
```

![example](https://github.com/schireson/htmxl/blob/main/docs/_static/readme.png)

## The Pitch

Essentially, HTM(x)L is an attempt to allow the declaration of Excel files in a (mostly) declarative
manner that separates the format that the document should take from the data being added to it.

The "normal" manner of producing Excel files essentially amounts to a series of imperitive
statements about what cells to modify to get the excel file you want. For any file of moderate
complexity, this leads to there being very little intuition about what the resulting Excel file will
actually look like.

Particularly once you start adding cell styling, or finding yourself inserting dynamically-sized
data (requiring a bunch of cell offset math), the relative ease of designing and visualizing the
template using a familiar idiom, HTML, can be make it much much easier to author and maintain these
kinds of templates.

## Features

General features include:

- HTML elements as metaphors for structures in the resulting Excel document

  Due to the obviously grid-oriented structure of Excel, the metaphors **can** sometimes be
  approximate, but should hopefully make intuitive sense!

  For example:

  - `<span>`: An inline-block element which pushes elements after it to the right
  - `<div>`: An block element which push elements after it downward
  - `<table>`: Self-explanatory!

  See the documentation about
  [elements](https://htmxl.readthedocs.io/en/latest/design/elements.html) for more details

- Styling

  Some commonly/obviously useful and style options like width/height (`style="width: 50px"`) or
  rowspan/colspan `colspan="2"` have been implemented, but there's no reason that various different
  options that make intuitive sense (like colors) could be implemented also

  See the documentation about [styling](https://htmxl.readthedocs.io/en/latest/design/styling.html)
  for more details

- Classes

  While inline color styles are not (yet) implemented, one can supply classes normally,
  `class="class1 class2"` and supply the definitions for those classes as inputs to the Workbook

  ``` python
  styles = [
      {"name": "odd", "pattern_fill": {"patternType": "solid", "fgColor": "FBEAFB"}},
  ]
  Workbook(styles=styles)
  ```

## Installation

There is no default parser (for HTML) included with a default installation of the package. We do
this for both backwards compatibility and future compatibility reasons.

In order to keep the base package lean when one opts to use one or the other parser, we include a
set of bundled parser-adaptor implementations for known supported parser libraries

To opt into the installation of the dependent library for the parser you chose:

``` bash
# Slower, but more permissive
pip install htmxl[beautifulsoup]

# Faster, but more strict
pip install htmxl[lxml]
```

By default, the package will detect installed parser libraries and choose the first one we find, so
a vanilla `Workbook()` instantiation should Just Work.

However, we encourage users to explicitly select their parser to avoid inadvertant selection of the
"wrong" parser at runtime (given that they have [template compatibility
issues](https://pytest-mock-resources.readthedocs.io/en/latest/compatbility.html))

``` python
from htmxl.compose import Workbook

workbook = Workbook(parser='beautifulsoup')
workbook = Workbook(parser='lxml')
```
