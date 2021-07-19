import io
import time

from htmxl.compose import Workbook

template = """
<head>{{ title }}</head>
<body>
  <div>
    Hello down there, {{ name }}!
  </div>
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
  </table>
</body>
"""

data = dict(
    title="Hello World",
    name="Bob",
    column_names=["A", "B"],
    rows=[{"a": str(i), "b": int(i)} for i in range(10000)],
)


def test_large_dataset():
    start = time.perf_counter()
    workbook = Workbook(parser="beautifulsoup")
    workbook.add_sheet_from_template(template=template, data=data)

    buffer = io.BytesIO()
    workbook.compose(buffer)
    end = time.perf_counter()

    bs4_duration = end - start

    start = time.perf_counter()
    workbook = Workbook(parser="lxml")
    workbook.add_sheet_from_template(template=template, data=data)

    buffer = io.BytesIO()
    workbook.compose(buffer)
    end = time.perf_counter()

    lxml_duration = end - start
    assert lxml_duration < bs4_duration
