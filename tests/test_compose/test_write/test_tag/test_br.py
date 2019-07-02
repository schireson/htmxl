from tests.utils import WriteTests


class WriteBr(WriteTests):
    fixture_dir = "tests/fixtures/templates/tags/br"


class TestAdjacent(WriteBr):
    template_file = "adjacent_br.html.jinja2"
    expected_result_file = "adjacent_br.xlsx"


class TestSingle(WriteBr):
    template_file = "single_br.html.jinja2"
    expected_result_file = "single_br.xlsx"
