import pytest

from htmxl.compose import Workbook
from tests.utils import WriteTests


class WriteDatalist(WriteTests):
    fixture_dir = "tests/fixtures/templates/tags/datalist"


class TestBasicListValidation(WriteDatalist):
    template_file = "basic_list_validation.html.jinja2"
    expected_result_file = "basic_list_validation.xlsx"

    def test_write_wat(self):
        result = self.load_source("lxml")

        validations = result._sheets[0].data_validations
        assert validations.count == 1
        assert validations.dataValidation[0].formula1 == '"foo,bar,baz"'


def test_invalid_datalist_reference():
    template = '<input list="options" />'

    wb = Workbook(parser="lxml")
    wb.add_sheet_from_template(template)
    with pytest.raises(ValueError) as e:
        wb.compose(None)

    assert "does not exist" in str(e.value)


def test_datalist_missing_id():
    template = "<datalist></datalist>"

    wb = Workbook(parser="lxml")
    wb.add_sheet_from_template(template)
    with pytest.raises(ValueError) as e:
        wb.compose(None)

    assert "requires an `id` attribute" in str(e.value)


def test_datalist_invalid_children():
    template = '<datalist id="ok"><span></span></datalist>'

    wb = Workbook(parser="lxml")
    wb.add_sheet_from_template(template)
    with pytest.raises(ValueError) as e:
        wb.compose(None)

    assert "only supports <option>" in str(e.value)
