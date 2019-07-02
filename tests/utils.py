import os

import openpyxl

from schireson_excel.compose import Workbook
from schireson_excel.compose.compat import BytesIO


class WriteTests:
    fixture_dir = ""
    template_file = ""
    expected_result_file = ""

    @property
    def expected_result(self):
        return openpyxl.load_workbook(os.path.join(self.fixture_dir, self.expected_result_file))

    @property
    def result(self):
        template_file = os.path.join(self.fixture_dir, self.template_file)
        wb = Workbook()
        wb.add_sheet_from_template_file(template_file)
        fileobj = BytesIO()
        wb.compose(fileobj)
        fileobj.seek(0)
        return openpyxl.load_workbook(fileobj)

    def test_sheets_num(self):
        assert len(self.result.worksheets) == len(self.expected_result.worksheets)

    def test_equality(self):
        result_worksheet = list(self.result.worksheets[0].rows)
        expected_worksheet = list(self.expected_result.worksheets[0].rows)

        assert len(result_worksheet) == len(expected_worksheet)
        for result_row, expected_row in zip(result_worksheet, expected_worksheet):
            assert len(result_row) == len(expected_row)
            for result_cell, expected_cell in zip(result_row, expected_row):
                assert result_cell.value == expected_cell.value
                assert result_cell.style == expected_cell.style
