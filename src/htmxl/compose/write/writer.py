"""A module dedicated to writing data to a workbook."""
import logging
from contextlib import contextmanager

import openpyxl.styles

from htmxl.compose.cell import Cell
from htmxl.compose.recording import Recording
from htmxl.compose.style import style_range
from htmxl.compose.write import elements

logger = logging.getLogger(__name__)


class Writer:
    def __init__(self, sheet, ref="A1"):
        self.current_cell = Cell(ref)
        self.sheet = sheet
        self._recordings = {}
        self._validations = {}

        self._auto_filter_set = False
        self._element_handlers = {
            "root": elements.write_body,
            "html": elements.write_body,
            "body": elements.write_body,
            "head": elements.write_head,
            "div": elements.write_div,
            "span": elements.write_span,
            "br": elements.write_br,
            "table": elements.write_table,
            "tr": elements.write_tr,
            "th": elements.write_th,
            "td": elements.write_td,
            "thead": elements.write_thead,
            "tbody": elements.write_tbody,
            "string": elements.write_string,
            "datalist": elements.create_datavalidation,
            "input": elements.write_input,
        }

    @property
    def row(self):
        return self.current_cell.row

    @property
    def col(self):
        return self.current_cell.col

    @property
    def ref(self):
        return self.current_cell.ref

    def write(self, element, styler):
        elements.write(writer=self, element=element, styler=styler)

    def get_cell(self, *, ref=None):
        if ref is None:
            ref = self.current_cell

        return self.sheet.cell(column=ref.col, row=ref.row)

    def write_cell(self, value, styler, style=None):
        cell = self.sheet.cell(column=self.col, row=self.row, value=value)

        if style:
            cell.style = styler.calculate_style(style)

        if self._recordings:
            for recording in self._recordings.values():
                recording.append(self.current_cell)

    def move_down(self, num=1):
        self.current_cell = Cell.from_location(col=self.col, row=self.row + num)

    def move_up(self, num=1):
        if self.row == 1:
            return

        self.current_cell = Cell.from_location(col=self.col, row=self.row - num)

    def move_left(self, num=1):
        if self.col == 1:
            return
        self.current_cell = Cell.from_location(col=self.col - num, row=self.row)

    def move_right(self, num=1):
        self.current_cell = Cell.from_location(col=self.col + num, row=self.row)

    def move(self, movement):
        movement_function = getattr(self, "move_{}".format(movement))
        movement_function()

    def move_to(self, col, row):
        self.current_cell = Cell.from_location(col=col, row=row)

    @contextmanager
    def record(self):
        recording = Recording()
        recording_id = recording.id()

        self._recordings[recording_id] = recording
        yield recording
        self.stop_recording(recording_id)

    def stop_recording(self, recording_id):
        del self._recordings[recording_id]

    def auto_filter(self, ref):
        if self._auto_filter_set:
            raise RuntimeError("You may only set autofilter once per sheet.")
        else:
            self.sheet.auto_filter.ref = ref
            self._auto_filter_set = True

    def style_inline(self, element, included_cells, inline_style):

        if inline_style.get("width"):
            column_refs = set()
            for cell in included_cells:
                column_refs.add(cell.col_ref)

            num_cols = len(column_refs)
            column_width = round(inline_style.get("width") / num_cols)

            for col_ref in column_refs:
                self.sheet.column_dimensions[col_ref].width = column_width

        if inline_style.get("height"):
            row_refs = set()
            for cell in included_cells:
                row_refs.add(cell.row)

            num_rows = len(row_refs)
            column_height = round(inline_style.get("height") / num_rows)

            for row_ref in row_refs:
                self.sheet.row_dimensions[row_ref].height = column_height

        if inline_style.get("text-align"):
            horizontal_alignment = inline_style.get("text-align")
            for cell in included_cells:
                self.sheet[cell.ref].alignment = self.sheet[
                    cell.ref
                ].alignment + openpyxl.styles.Alignment(horizontal=horizontal_alignment)

        if inline_style.get("vertical-align"):
            vertical_alignment = inline_style.get("vertical-align")
            for cell in included_cells:
                self.sheet[cell.ref].alignment = self.sheet[
                    cell.ref
                ].alignment + openpyxl.styles.Alignment(vertical=vertical_alignment)

        if inline_style.get("data-wrap-text"):
            if inline_style.get("data-wrap-text").lower() == "true":
                for cell in included_cells:
                    logger.debug("Setting wrapText=True for cell {}".format(cell))
                    self.sheet[cell.ref].alignment = self.sheet[
                        cell.ref
                    ].alignment + openpyxl.styles.Alignment(wrapText=True)

    def style_range(self, reference_style, cell_range):
        style_range(self.sheet, reference_style, cell_range)

    def add_validation(self, id, validation):
        self._validations[id] = validation
        self.sheet.add_data_validation(validation)

    def add_validation_to_cell(self, validation_name):
        validation = self._validations.get(validation_name)
        if not validation:
            raise ValueError(f"<datalist> validation with name '{validation_name}' does not exist")

        current_cell = self.get_cell()
        validation.add(current_cell)
