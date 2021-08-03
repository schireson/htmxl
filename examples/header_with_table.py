import datetime

from htmxl.compose import Workbook

with open('examples/header_with_table.jinja2') as f:
    template = f.read()

data = [
    {
        "State": "New York",
        "City": "New York City",
        "Date": datetime.date(2019, 1, 1),
        "Other Date": datetime.date(2016, 3, 15),
        "Count": 55,
    },
    {
        "State": "Texas",
        "City": "Austin",
        "Date": datetime.date(2016, 5, 28),
        "Other Date": datetime.date(2015, 3, 15),
        "Count": 500,
    },
    {
        "State": "Massachussetts",
        "City": "Cambridge",
        "Date": datetime.date(2019, 3, 15),
        "Other Date": datetime.date(2014, 3, 15),
        "Count": 34,
    },
]

column_names = list(data[0].keys())


STYLES = [
    {"name": "odd", "pattern_fill": {"patternType": "solid", "fgColor": "FBEAFB"}},
    {"name": "even", "pattern_fill": {"patternType": "solid", "fgColor": "DFE7F8"}},
    {
        "name": "odd-date",
        "pattern_fill": {"patternType": "solid", "fgColor": "FBEAFB"},
        "number_format": "yyyy-mm-dd",
    },
    {
        "name": "even-date",
        "pattern_fill": {"patternType": "solid", "fgColor": "DFE7F8"},
        "number_format": "yyyy-mm-dd",
    },
]


if __name__ == "__main__":
    import sys
    import logging

    logging.basicConfig(level=logging.DEBUG)
    filename = sys.argv[1]
    workbook = Workbook(styles=STYLES)
    workbook.add_sheet_from_template(
        template=template,
        data=dict(
            title="Random Cities with Data",
            subject="Cities",
            rows=data,
            column_names=column_names,
        ),
    )

    workbook.compose(filename)
