from tests.utils import WriteTests


class WriteTh(WriteTests):
    fixture_dir = "tests/fixtures/templates/tags/th"


class TestColspanMergesCells(WriteTh):
    template_file = "colspan_merges.html.jinja2"
    expected_result_file = "colspan_merges.xlsx"


class TestRowspanMergesCells(WriteTh):
    template_file = "rowspan_merges.html.jinja2"
    expected_result_file = "rowspan_merges.xlsx"


class TestRowspanContainedRow(WriteTh):
    template_file = "rowspan_contained_row.html.jinja2"
    expected_result_file = "rowspan_contained_row.xlsx"
