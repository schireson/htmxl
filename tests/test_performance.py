import io
import time

from htmxl.compose import Workbook


def test_large_dataset():
    workbook = Workbook()
    workbook.add_sheet_from_template(
        template="""
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
        """,
        data=dict(
            title="Hello World",
            name="Bob",
            column_names=["A", "B"],
            rows=[{"a": str(i), "b": int(i)} for i in range(10000)],
        ),
    )

    buffer = io.BytesIO()

    start = time.perf_counter()
    workbook.compose(buffer)
    end = time.perf_counter()

    duration = end - start
    print(duration)
    assert duration < 3
