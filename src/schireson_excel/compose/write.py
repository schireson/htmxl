"""A module dedicated to writing data to a workbook."""
import ast
import datetime
import functools
import logging
import string
from contextlib import contextmanager

import bs4
import bs4.element
import openpyxl.styles
import pendulum

import schireson_excel.compose.attributes
from schireson_excel.compose.style import style_range

logger = logging.getLogger(__name__)


TOP_RIGHT = "top-right"
BOTTOM_RIGHT = "bottom-right"
BOTTOM_LEFT = "bottom-left"

_type_map = {
    None: str,
    "str": str,
    "int": int,
    "float": float,
    "date": lambda x: pendulum.parse(x).date(),
    "datetime": lambda x: pendulum.parse(x),
    "bool": ast.literal_eval,
}


class Writer:
    def __init__(self, sheet, ref="A1"):
        self.current_cell = Cell(ref)
        self.sheet = sheet
        self._cells = {self.current_cell.ref: self.current_cell}
        self._recordings = {}

        self._auto_filter_set = False

    @property
    def row(self):
        return self.current_cell.row

    @property
    def col(self):
        return self.current_cell.col

    @property
    def ref(self):
        return self.current_cell.ref

    def get_cell(self, ref):
        cell = self._cells.get(ref)
        if cell is None:
            cell = Cell(ref)
            self._cells[ref] = cell

    def write_cell(self, value, style=None):

        cell = self.sheet.cell(column=self.col, row=self.row, value=value)

        if style:
            cell.style = style

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
        recording = []
        recording_id = id(recording)

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


def write(element, writer, styler, style=None):
    if type(element) == bs4.BeautifulSoup:
        logger.debug("Writing < body > at {}".format(writer.ref))
        for item in element.body:
            write(item, writer, styler)

    if type(element) == bs4.element.Tag:

        if element.name == "div":
            write_div(element, writer, styler, style)

        if element.name == "span":
            write_span(element, writer, styler, style)

        elif element.name == "br":
            logger.debug("Writing <br> at {}".format(writer.ref))
            row = writer.row
            col = writer.col
            write("", writer, styler, style)
            writer.move_to(col=col, row=row)
            writer.move_down()

        elif element.name == "table":
            write_table(element, writer, styler, style)

        elif element.name == "tr":
            write_tr(element, writer, styler, style)

        elif element.name == "th":
            write_th(element, writer, styler, style)

        elif element.name == "td":
            write_td(element, writer, styler, style)

        elif element.name == "thead":
            write_thead(element, writer, styler, style)

        elif element.name == "tbody":
            write_tbody(element, writer, styler, style)

    elif type(element) == bs4.element.NavigableString:
        logger.debug("Writing navigable string at {}".format(writer.ref))
        value = element.strip()
        if value:
            write(value, writer, styler, style)

    else:
        if isinstance(element, (str, int, float, bool, datetime.date)):
            write_value(element, writer, styler, style)


class Cell:
    def __init__(self, ref="A1"):
        for idx, char in enumerate(ref):
            if char.isdigit():
                col = ref[0:idx]
                row = int(ref[idx:])
                break
        self._col = col
        self._row = row

    @classmethod
    def from_location(cls, col, row):
        ref = "{}{}".format(alphabet[col - 1], row)
        return cls(ref)

    @property
    def row(self):
        return int(self._row)

    @property
    def row_ref(self):
        return str(self._row)

    @property
    def col_ref(self):
        return self._col

    @property
    def col(self):
        return alphabet.index(self._col) + 1

    @property
    def ref(self):
        return "{}{}".format(self._col, self._row)

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.ref)


def return_cursor(strategy):
    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(element, writer, styler, style):
            if strategy == BOTTOM_LEFT:
                column = writer.col
                result = fn(element, writer, styler, style)
                writer.move_to(col=column, row=writer.row)
                writer.move_down()

            elif strategy == BOTTOM_RIGHT:
                result = fn(element, writer, styler, style)
                writer.move_right()

            elif strategy == TOP_RIGHT:
                row = writer.row
                result = fn(element, writer, styler, style)
                writer.move_to(col=writer.col, row=row)
                writer.move_right()

            else:
                raise ValueError("Strategy {} unknown".format(strategy))

            return result

        return wrapped

    return wrapper


def inline_styleable(fn):
    @functools.wraps(fn)
    def wrapper(element, writer, styler, style):
        element, recording = fn(element, writer, styler, style)
        writer.style_inline(
            element=element, included_cells=recording, inline_style=styler.get_inline_style(element)
        )
        return element, recording

    return wrapper


def write_value(element, writer, styler, style):
    logger.debug("Writing <value> at {}".format(writer.ref))
    writer.write_cell(element, style)


@return_cursor(TOP_RIGHT)
@inline_styleable
def write_td(element, writer, styler, style):
    logger.debug("Writing <td> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        data_type = _type_map[element.attrs.get("data-type")]
        logger.debug("Setting cell {} to {}".format(writer.ref, data_type))
        write(data_type(element.text.strip()), writer, styler, style)

    return element, recording


@return_cursor(BOTTOM_LEFT)
@inline_styleable
def write_tr(element, writer, styler, style):
    logger.debug("Writing <tr> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        for td in element:
            write(td, writer, styler, style)

    return element, recording


@return_cursor(TOP_RIGHT)
@inline_styleable
def write_th(element, writer, styler, style):
    logger.debug("Writing <th> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        write(element.text.strip(), writer, styler, style)

        colspan = int(element.attrs.get("colspan", 1))
        rowspan = int(element.attrs.get("rowspan", 1))

        # If we want this cell to span more than one row or column
        # we can traverse to the maximum row and column and write some blank data.
        # This will expand the recorded "bounding ref" to the proper location
        # This also then supports the "TOP_RIGHT" return cursor behavior.
        if rowspan > 1 or colspan > 1:
            writer.move_right(colspan - 1)
            writer.move_down(rowspan - 1)
            write("", writer, styler, style)

    if len(recording) > 1:
        if style:
            merge_ref = get_bounding_ref(recording)
            reference_style = styler.named_styles[style]
            writer.sheet.merge_cells(merge_ref)
            writer.style_range(reference_style, merge_ref)

    return element, recording


@return_cursor(BOTTOM_LEFT)
@inline_styleable
def write_table(element, writer, styler, style):
    logger.debug("Writing <table> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    autofilter = element.get(schireson_excel.compose.attributes.DATA_AUTOFILTER, "false")

    with writer.record() as recording:
        for sub_component in element:
            write(sub_component, writer, styler, style)

    if autofilter == "true":
        bounding_ref = get_bounding_ref(recording)
        writer.auto_filter(bounding_ref)

    return element, recording


@inline_styleable
def write_thead(element, writer, styler, style):
    logger.debug("Writing <thead> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        for sub_component in element:
            write(sub_component, writer, styler, style)

    return element, recording


@inline_styleable
def write_tbody(element, writer, styler, style):
    logger.debug("Writing <tbody> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        for sub_component in element:
            write(sub_component, writer, styler, style)

    return element, recording


@return_cursor(BOTTOM_LEFT)
@inline_styleable
def write_div(element, writer, styler, style):
    logger.debug("Writing <div> at {}".format(writer.ref))
    style = styler.get_style(element) or style

    with writer.record() as recording:
        for item in element:
            write(item, writer, styler, style)

    return element, recording


@return_cursor(TOP_RIGHT)
@inline_styleable
def write_span(element, writer, styler, style):
    logger.debug("Writing <span> at {}".format(writer.ref))
    with writer.record() as recording:
        for item in element:
            style = styler.get_style(element) or style
            write(item, writer, styler, style)

    return element, recording


def _column_letters():
    multiplyer = 1
    while True:
        for letter in string.ascii_uppercase:
            yield letter * multiplyer
        multiplyer += 1


def get_bounding_ref(cells):
    min_row = min(cell.row for cell in cells)
    min_col = min(cell.col for cell in cells)
    max_row = max(cell.row for cell in cells)
    max_col = max(cell.col for cell in cells)

    min_cell = Cell.from_location(row=min_row, col=min_col)

    max_cell = Cell.from_location(row=max_row, col=max_col)

    return "{}:{}".format(min_cell.ref, max_cell.ref)


class _Alphabet:
    def __init__(self, starting_length=26):
        self.letter_list = []
        self.column_letter_factory = _column_letters()
        for _ in range(starting_length):
            self._generate_more_letters()

    def index(self, value):
        num_letters = len(self.letter_list)
        if num_letters < len(value) * 26:
            for i in range(num_letters, len(value) * 26):
                self._generate_more_letters()

        return self.letter_list.index(value)

    def __getitem__(self, item):
        if len(self.letter_list) + 1 < item:
            for i in range(item - len(self.letter_list) + 1):
                self.letter_list.append(next(self.column_letter_factory))
        return self.letter_list[item]

    def _generate_more_letters(self):
        self.letter_list.append(next(self.column_letter_factory))

    def __repr__(self):
        return "Alphabet(num_letters={})".format(len(self.letter_list))


alphabet = _Alphabet()
