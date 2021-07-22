from dataclasses import dataclass

from htmxl.compose.cell import Cell


@dataclass
class Recording:
    count: int = 0

    min_row: int = 1
    min_col: int = 1
    max_row: int = 1
    max_col: int = 1

    def append(self, cell):
        cell_row = cell.row
        cell_col = cell.col

        if cell_row < self.min_row:
            self.min_row = cell_row

        if cell_col < self.min_col:
            self.min_col = cell_col

        if cell_row > self.max_row:
            self.max_row = cell_row

        if cell_col > self.max_col:
            self.max_col = cell_col

        self.count += 1

    def id(self):
        return id(self)

    def __len__(self):
        return self.count

    @property
    def bounding_cells(self):
        return (
            Cell.from_location(row=self.min_row, col=self.min_col),
            Cell.from_location(row=self.max_row, col=self.max_col),
        )

    @property
    def bounding_ref(self):
        min_cell, max_cell = self.bounding_cells
        return f"{min_cell.ref}:{max_cell.ref}"
