import ast
import logging

import pendulum

import htmxl.compose.attributes
from htmxl.compose.write.decorators import CursorStrategy, return_cursor

logger = logging.getLogger(__name__)


_type_map = {
    None: str,
    "str": str,
    "int": int,
    "float": float,
    "date": lambda x: pendulum.parse(x).date(),
    "datetime": lambda x: pendulum.parse(x),
    "bool": ast.literal_eval,
}


def write(element, writer, styler, style=None):
    tag = element.name
    try:
        handler = writer._element_handlers[tag]
    except KeyError:
        raise RuntimeError(f"Encountered unhandled or unimplemented tag {tag}.")
    else:
        handler(element, writer, styler, style)


def write_body(element, writer, styler, style):
    logger.debug("Writing < body > at {}".format(writer.ref))
    for item in element.content():
        write(item, writer, styler)


def write_head(element, writer, styler, style):
    tag = element.name
    if tag in {"head", "title"}:
        for item in element.content():
            write_head(item, writer, styler, style)
    elif tag == "string":
        writer.sheet.title = element.text
    else:
        raise RuntimeError(f"Encountered unhandled or unimplemented tag {tag}.")


def write_br(element, writer, styler, style):
    logger.debug("Writing <br> at {}".format(writer.ref))
    row = writer.row
    col = writer.col
    value = writer.get_cell(writer.current_cell).value
    if value:
        writer.move_down()
        writer.move_down()
    else:
        write_value("", writer, styler, style)
        writer.move_to(col=col, row=row)
        writer.move_down()


def write_value(element, writer, styler, style):
    logger.debug("Writing <value> at {}".format(writer.ref))
    writer.write_cell(element, styler, style)


@return_cursor(CursorStrategy.top_right)
def write_td(element, writer, styler, style):
    logger.debug("Writing <td> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        data_type = _type_map[element.attrs.get("data-type")]
        logger.debug("Setting cell {} to {}".format(writer.ref, data_type))
        write_value(data_type(element.text.strip()), writer, styler, style)

    return element, recording


@return_cursor(CursorStrategy.bottom_left)
def write_tr(element, writer, styler, style):
    logger.debug("Writing <tr> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        for td in element.content():
            write(td, writer, styler, style)

    return element, recording


@return_cursor(CursorStrategy.top_right)
def write_th(element, writer, styler, style):
    logger.debug("Writing <th> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        data_type = _type_map[element.attrs.get("data-type")]
        logger.debug("Setting cell {} to {}".format(writer.ref, data_type))
        write_value(data_type(element.text.strip()), writer, styler, style)

        colspan = int(element.attrs.get("colspan", 1))
        rowspan = int(element.attrs.get("rowspan", 1))

        # If we want this cell to span more than one row or column
        # we can traverse to the maximum row and column and write some blank data.
        # This will expand the recorded "bounding ref" to the proper location
        # This also then supports the `CursorStrategy.top_right` return cursor behavior.
        if rowspan > 1 or colspan > 1:
            writer.move_right(colspan - 1)
            writer.move_down(rowspan - 1)
            write_value("", writer, styler, style)

    if len(recording) > 1:
        if rowspan or colspan:
            merge_ref = recording.bounding_ref
            writer.sheet.merge_cells(merge_ref)
            if style:
                style_name = styler.calculate_style(style)
                reference_style = styler.named_styles[style_name]
                writer.style_range(reference_style, merge_ref)

    return element, recording


@return_cursor(CursorStrategy.bottom_left)
def write_table(element, writer, styler, style):
    logger.debug("Writing <table> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    autofilter = element.get(htmxl.compose.attributes.DATA_AUTOFILTER, "false")

    with writer.record() as recording:
        for sub_component in element.content():
            write(sub_component, writer, styler, style)

    if autofilter == "true":
        bounding_ref = recording.bounding_ref
        writer.auto_filter(bounding_ref)

    return element, recording


@return_cursor(CursorStrategy.bottom_left)
def write_thead(element, writer, styler, style):
    logger.debug("Writing <thead> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        for sub_component in element.content():
            write(sub_component, writer, styler, style)

    return element, recording


@return_cursor(CursorStrategy.bottom_left)
def write_tbody(element, writer, styler, style):
    logger.debug("Writing <tbody> at {}".format(writer.ref))
    style = styler.get_style(element) or style
    with writer.record() as recording:
        for sub_component in element.content():
            write(sub_component, writer, styler, style)

    return element, recording


@return_cursor(CursorStrategy.bottom_left)
def write_div(element, writer, styler, style):
    logger.debug("Writing <div> at {}".format(writer.ref))
    style = styler.get_style(element) or style

    with writer.record() as recording:
        for item in element.content():
            write(item, writer, styler, style)

    return element, recording


@return_cursor(CursorStrategy.top_right)
def write_span(element, writer, styler, style):
    logger.debug("Writing <span> at {}".format(writer.ref))
    with writer.record() as recording:
        for item in element.content():
            style = styler.get_style(element) or style
            write(item, writer, styler, style)

    return element, recording


def write_string(element, writer, styler, style):
    write_value(element.text, writer, styler, style)