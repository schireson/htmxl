from pprint import pprint

from htmxl.compose import Workbook

data = dict(
    title="Hello World",
    name="Bob",
    column_names=["A", "B"],
    rows=[{"a": str(i), "b": int(i)} for i in range(10)],
)


def test_large_dataset():
    with open(f"{__file__}.jinja2") as f:
        template = f.read()

    workbook = Workbook(parser="lxml")
    workbook.add_sheet_from_template(template=template, data=data)
    workbook.write()
    pprint(list(workbook.worksheets[0].writer.vdom.rows()))
    raise
