import setuptools
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

PACKAGES = find_packages(where='.')

setuptools.setup(
    name='blockapi',
    version='0.0.15',
    author='Devmons s.r.o.',
    description='BlockAPI library',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=PACKAGES,
    install_requires=[
        'requests', 
        'pytz', 
        'python-dateutil',
        'coinaddrng',
        'cfscrape'
    ],
)

