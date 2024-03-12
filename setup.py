import setuptools
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

PACKAGES = find_packages(where='.')

__version__ = "0.41.0"

setuptools.setup(
    name='blockapi',
    version=__version__,
    author='Devmons s.r.o.',
    description='BlockAPI library',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=PACKAGES,
    install_requires=[
        'requests==2.31.0',
        'pytz>=2019.2',
        'python-dateutil>=2.8.0',
        'coinaddrng==1.1.1',
        'cfscrape>=2.0.8',
        'ethereum_input_decoder>=0.2.2',
        'web3>=5.2.2,<6.0.0',
        'bs4>=0.0.1',
        'lxml>=4.4.1',
        'pydantic>=1.10.2',
        'marko==1.3.0',
        'fake_useragent>=1.1.3',
        'pytest',
        'pytest-vcr',
        'requests_mock>=1.9.3',
    ],
)
