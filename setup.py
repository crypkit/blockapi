import setuptools
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

PACKAGES = find_packages(where='.')

setuptools.setup(
    name='blockapi',
    version='0.0.64',
    author='Devmons s.r.o.',
    description='BlockAPI library',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=PACKAGES,
    install_requires=[
        'requests>=2.22.0',
        'pytz>=2019.2',
        'python-dateutil>=2.8.0',
        'coinaddrng==1.0.25',
        'cfscrape>=2.0.8',
        'gevent>=1.4.0',
        'ethereum_input_decoder>=0.2.2',
        'web3>=5.2.2',
        'bs4>=0.0.1',
        'lxml>=4.4.1',
        'pytest',
        'pytest-vcr'
    ],
)

