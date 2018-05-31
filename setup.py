#!/usr/bin/env python

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='pscb',
    version='1.0.0',
    description='Software required to run PSCB Exhibit',  # Required
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://flexhibit.com',
    author='Ryan Mills',
    author_email='ryan@flexhibit.com',

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.6',
    ],
)
