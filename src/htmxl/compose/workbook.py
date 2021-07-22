"""A module dedicated to the core Workbook class which is a wrapper around the openpyxl workbook."""

import logging
import uuid

import jinja2
import openpyxl

from htmxl.compose.style import Styler
from htmxl.compose.write import Writer
from htmxl.token import get_parser

logger = logging.getLogger(__name__)

jinja_env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True, autoescape=False)


class Workbook:
    def __init__(self, styles=None, workbook_kwargs=None, *, parser=None):
        if workbook_kwargs is None:
            workbook_kwargs = {}

        self.wb = openpyxl.workbook.Workbook(**workbook_kwargs)
        self.wb.remove(self.wb.worksheets[0])
        self.worksheets = []
        self.styler = Styler(self.wb, styles)
        self.parser = parser

    def new_worksheet(self, parser=None):
        worksheet = Worksheet(styler=self.styler, wb=self.wb, parser=parser or self.parser)
        self.worksheets.append(worksheet)

        return worksheet

    def add_sheet_from_template_file(self, template_file, data=None):
        if data is None:
            data = {}

        with open(template_file, "r") as f:
            return self.add_sheet_from_template(template=f.read(), data=data)

    def add_sheet_from_template(self, template, data=None, parser=None):
        if data is None:
            data = {}

        worksheet = self.new_worksheet(parser=parser or self.parser)
        worksheet.template = jinja_env.from_string(template)
        worksheet.data = data
        return worksheet

    def write(self):
        logger.debug("Writing sheets for {}".format(self.wb))
        for sheet in self.worksheets:
            sheet.write()

    def save(self, file_path):
        logger.debug("Saving {} to {}".format(self.wb, file_path))
        self.wb.save(file_path)

    def compose(self, file_path):
        logger.debug("Composing {}".format(self.wb))
        self.write()
        self.save(file_path)


class Worksheet:
    def __init__(self, wb, styler, parser=None):
        self.sheet_name = str(uuid.uuid4())[0:8]
        self.writer = Writer(wb.create_sheet(self.sheet_name))
        self.styler = styler
        self.data = {}
        self.template = None
        self.parser = parser

    @property
    def worksheet(self):
        return self.writer.sheet

    @property
    def tree(self):
        logger.debug(
            "Parsing the template into a tree of nodes for sheet <{}>".format(self.sheet_name)
        )
        parser = get_parser(self.parser)
        return parser.parse_str(self.rendered)

    @property
    def rendered(self):
        logger.debug("Rendering sheet <{}>".format(self.sheet_name))
        return self.template.render(self.data)

    def write(self):
        logger.debug("Writing sheet <{}>".format(self.sheet_name))
        self.writer.write(element=self.tree, styler=self.styler)
