import pytest


@pytest.mark.parametrize("name", ["Writer", "write", "Cell", "Styler", "Workbook", "Worksheet"])
def test_import_name(name):
    import htmxl.compose

    assert hasattr(htmxl.compose, name)
