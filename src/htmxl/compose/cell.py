import functools

from htmxl.alphabet import alphabet


@functools.lru_cache()
def calculate_row_col(ref):
    for idx, char in enumerate(ref):
        if char.isdigit():
            row = int(ref[idx:])
            col = ref[0:idx]
            break

    return (col, row)


class Cell:
    def __init__(self, ref="A1"):
        col, row = calculate_row_col(ref)

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
