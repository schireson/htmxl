import io

from htmxl.compose import Workbook

data = dict(
    title="Hello World",
    name="Bob",
    column_names=["A", "B"],
    rows=[{"a": str(i), "b": int(i)} for i in range(10000)],
)


def test_sheet_with_empty_elements():
    with open("tests/test_empty_elements.jinja2") as f:
        template = f.read()

    workbook = Workbook(parser="lxml")
    workbook.add_sheet_from_template(template=template, data=data)

    buffer = io.BytesIO()
    workbook.compose(buffer)
