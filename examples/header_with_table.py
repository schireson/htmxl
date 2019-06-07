import datetime
import textwrap

from schireson_excel.compose import Workbook, Worksheet

template = textwrap.dedent(
    """\
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
        <div>
            <span style="width: 5ch;">__BLANK__</span>
            <span>Table Subject</span>
            <span>{{ subject }}</span>
        </div>
        <br>
        <div>
            <span></span>
            <span>
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
                                <td style="width: 30ch;" class="{{ loop.cycle('odd', 'even')}}">{{ row.State }}</td>
                                <td style="width: 30ch;" class="{{ loop.cycle('odd', 'even')}}">{{ row.City }}</td>
                                <td data-type="date" style="width: 30ch;" class="{{ loop.cycle('odd-date', 'even-date')}}">{{ row.Date}}</td>
                                <td data-type="date" style="width: 30ch;" class="{{ loop.cycle('odd-date', 'even-date')}}">{{ row["Other Date"]}}</td>
                                <td data-type="int" style="width: 30ch;" class="{{ loop.cycle('odd', 'even')}}">{{ row.Count }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table
            </span>
        </div>
    </body>
"""
)

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
