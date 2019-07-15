from setuptools import find_packages, setup

INSTALL_REQUIRES = [
    "beautifulsoup4>=4.6",
    "openpyxl==2.5",  # See https://bitbucket.org/openpyxl/openpyxl/issues/1249/cannot-convert-my-type-to-excel
    "jinja2>=2.10",
    "pendulum>=1.0",
]

TESTING_REQUIRES = [
    "lucha",
    "pytest",
    "pytest-cov",
    "isort",
    "black",
    "flake8",
    "pydocstyle",
]

DOCS_REQUIRES = ["sphinx", "sphinx_rtd_theme", "m2r"]

setup(
    name="schireson-excel",
    version="0.7.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=INSTALL_REQUIRES,
    extras_require={"testing": TESTING_REQUIRES, "docs": DOCS_REQUIRES},
)
