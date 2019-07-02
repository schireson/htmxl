from tests.utils import WriteTests


class WriteDiv(WriteTests):
    fixture_dir = "tests/fixtures/templates/tags/div"


class TestAdjacentDivs(WriteDiv):
    template_file = "adjacent_divs.html.jinja2"
    expected_result_file = "adjacent_divs.xlsx"


class TestContainedDivs(WriteDiv):
    template_file = "contained_divs.html.jinja2"
    expected_result_file = "contained_divs.xlsx"


class TestNoContent(WriteDiv):
    template_file = "div_no_content.html.jinja2"
    expected_result_file = "div_no_content.xlsx"
