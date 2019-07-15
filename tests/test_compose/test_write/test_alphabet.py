import pytest

from schireson_excel.compose.write import _column_letters


@pytest.mark.this
def test_column_letter_factory():
    result = []
    _func = _column_letters()
    for i in range(30):
        result.append(next(_func))
    assert result == [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "AA",
        "AB",
        "AC",
        "AD",
    ]
