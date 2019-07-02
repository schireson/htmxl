try:
    from io import BytesIO  # noqa
except ImportError:
    from StringIO import StringIO as BytesIO  # noqa
