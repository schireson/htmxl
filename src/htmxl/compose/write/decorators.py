import enum
import functools


@enum.unique
class CursorStrategy(enum.Enum):
    top_right = "top-right"
    bottom_right = "bottom-right"
    bottom_left = "bottom-left"


def return_cursor(strategy):
    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(element, writer, styler, style):
            if strategy == CursorStrategy.bottom_left:
                # Must be determined before we potentially change the location by `fn`.
                column = writer.col
                row = writer.row

                element, recording = fn(element, writer, styler, style)

                if recording:
                    _, bottom_right = recording.bounding_cells
                    row = bottom_right.row

                writer.move_to(col=column, row=row)
                writer.move_down()

            elif strategy == CursorStrategy.bottom_right:
                element, recording = fn(element, writer, styler, style)
                writer.move_right()

            elif strategy == CursorStrategy.top_right:
                row = writer.row
                element, recording = fn(element, writer, styler, style)
                writer.move_to(col=writer.col, row=row)
                writer.move_right()

            else:
                raise ValueError("Strategy {} unknown".format(strategy))

            writer.style_inline(
                element=element,
                included_cells=recording,
                inline_style=styler.get_inline_style(element),
            )

            return element, recording

        return wrapped

    return wrapper


def inline_styleable(fn):
    @functools.wraps(fn)
    def wrapper(element, writer, styler, style):
        element, recording = fn(element, writer, styler, style)
        return element, recording

    return wrapper
