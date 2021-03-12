import openpyxl
import pendulum


def test_openpyxl_version():
    """Validate the installed version of openpyxl is compatible with pendulum.

    This test just needs to pass to verify functionality.
    """

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "OpenPyXL Bug"

    mydate = pendulum.parse("2019-04-01")
    print(f"Date: {mydate}")

    cell = ws.cell(row=1, column=1)

    # ===== ERROR OCCURS ON THE LINE BELOW =====
    cell.value = mydate
    cell.number_format = "DD MMM YYYY"
