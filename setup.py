from setuptools import setup, find_packages


INSTALL_REQUIRES = [
    'beautifulsoup4~=4.6',
    'openpyxl~=2.5',
    'jinja2~=2.10',
    'pendulum~=2.0',
]

TESTING_REQUIRES = [
    'lucha',
    'pytest',
    'pytest-cov',
    'isort',
    'black',
    'flake8',
    'pydocstyle',
]

DOCS_REQUIRES = [
    'sphinx',
    'sphinx_rtd_theme',
]

setup(
    name='schireson-excel',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'testing': TESTING_REQUIRES,
        'docs': DOCS_REQUIRES,
    }
)
