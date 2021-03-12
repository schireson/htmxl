import pendulum
from openpyxl.cell import cell
from openpyxl.styles import numbers

# Monkeypatch openpyxl to include pendulum types, although per
# https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1249, it'd be preferable
# if they altered their checks to be cross-compatible with other subclasses.
cell.TIME_TYPES = (*cell.TIME_TYPES, pendulum.DateTime, pendulum.Date)
cell.TIME_FORMATS = {
    **cell.TIME_FORMATS,
    pendulum.DateTime: numbers.FORMAT_DATE_DATETIME,
    pendulum.Date: numbers.FORMAT_DATE_YYYYMMDD2,
    pendulum.Time: numbers.FORMAT_DATE_TIME6,
    pendulum.Duration: numbers.FORMAT_DATE_TIMEDELTA,
}
