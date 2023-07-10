import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.4'
PACKAGE_NAME = 'cleanup_tables'
AUTHOR = 'ZINA Team'
AUTHOR_EMAIL = 'support.zina@nokia.com'
DESCRIPTION = 'Cleanup tables'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"
INSTALL_REQUIRES = [
    'python-dateutil'
]
PACKAGES = [
    PACKAGE_NAME
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    include_package_data=True
)
