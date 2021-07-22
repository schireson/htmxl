import functools

from htmxl.alphabet import alphabet


@functools.lru_cache()
def split_col_row(ref):
    """Split the letter and number components of a cell reference.

    Examples:
        >>> split_col_row('A1')
        ('A', 1)
        >>> split_col_row('B100')
        ('B', 100)
        >>> split_col_row('CC12')
        ('CC', 12)
    """
    head = ref.rstrip("0123456789")
    tail = ref[len(head) :]
    return head, int(tail)


class Cell:
    def __init__(self, ref="A1"):
        col, row = split_col_row(ref)

        self.row = row
        self.row_ref = str(row)

        self.col = alphabet.index(col) + 1
        self.col_ref = col

    @classmethod
    def from_location(cls, col, row):
        col = alphabet[col - 1]
        ref = f"{col}{row}"
        return cls(ref)

    @property
    def ref(self):
        return f"{self.col_ref}{self.row}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.ref}')"
