import pytest


@pytest.mark.parametrize("name", ["Writer", "write", "Cell", "Styler", "Workbook", "Worksheet"])
def test_import_name(name):
    import schireson_excel.compose

    assert hasattr(schireson_excel.compose, name)
