import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'cleanup_tables'
AUTHOR = 'ZINA Team'
AUTHOR_EMAIL = 'support.zina@nokia.com'
# URL = 'github url'

# LICENSE = 'MIT'
DESCRIPTION = 'Cleanup tables'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'python-dateutil==2.8.2'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # url=URL,
    install_requires=INSTALL_REQUIRES,
    # license=LICENSE,
    packages=[
        PACKAGE_NAME
    ],
    include_package_data=True
)
