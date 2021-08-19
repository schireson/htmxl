from tests.utils import WriteTests


class WriteTd(WriteTests):
    fixture_dir = "tests/fixtures/templates/tags/td"


class TestTd(WriteTd):
    template_file = "td.html.jinja2"
    expected_result_file = "td.xlsx"
    styles = [
        {"name": "regular", "font": {"name": "Arial", "size": 10}},
        {"name": "bold", "font": {"name": "Arial", "size": 10, "bold": True}},
        {"name": "text", "number_format": "@"},
        {"name": "red-font", "font": {"color": "FFFF0000"}},
    ]


class TestTdStyleAppliedToNestedElements(WriteTd):
    template_file = "td_nested_styles.html.jinja2"
    expected_result_file = "td_nested_styles.xlsx"
    styles = [
        {"name": "regular", "font": {"name": "Arial", "size": 10}},
        {"name": "bold", "font": {"name": "Arial", "size": 10, "bold": True}},
        {"name": "text", "number_format": "@"},
        {"name": "red-font", "font": {"color": "FFFF0000"}},
    ]
