import setuptools
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

PACKAGES = find_packages(where='.')

__version__ = "2.10.4"

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
        'requests>=2.28,<3.0',
        'python-dateutil>=2.8.0',
        'cytoolz>=0.12.0',
        'eth-utils>=2.0.0',
        'coinaddrng==1.1.1',
        'pydantic>=1.10.2',
        'fake_useragent>=1.1.3',
        'pytest',
        'pytest-vcr',
        'requests_mock>=1.9.3',
        'attrs>=17.4.0,<23.0.0',
        'base58>=2.1.0',
        # vcrpy incompatible with 3.14, remove once vcrpy>8.1.1 is out
        'aiohttp<3.14',
    ],
    url="https://github.com/crypkit/blockapi",
)
