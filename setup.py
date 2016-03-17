#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('treepoem')


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'Pillow',
]

test_requirements = [
    'Pillow',
]

setup(
    name='treepoem',
    version=version,
    description="A very simple Python wrapper around BWIPP.",
    long_description=readme + '\n\n' + history,
    author="Christian Muirhead",
    author_email='xtian@babbageclunk.com',
    maintainer="Julius Seporaitis",
    maintainer_email="julius@yplanapp.com",
    url='https://github.com/YPlan/treepoem',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_dir={
        'treepoem': 'treepoem',
    },
    include_package_data=True,
    install_requires=requirements,
    license="AGPLv3+",  # to be determined
    zip_safe=False,
    keywords='barcode bwipp ghostscript',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
