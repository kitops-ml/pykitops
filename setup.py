#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import re

from setuptools import setup # type: ignore
from typing import Any

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

with io.open('kitops/__init__.py', 'rt', encoding='utf8') as f:
    version: re.Match[str] | None = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        f.read(),
        re.MULTILINE
    )
    if version is not None:
        version_str: str | Any = version.group(1)

requirements: dict[str, list | None] = {'base': None, 'development': None}
for k in requirements:
    with open("requirements/{}.in".format(k)) as f:
        requirements[k] = list(filter(lambda x: bool(x.strip()) and not x.strip().startswith('-r '), f.read().splitlines()))

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='kitops',
    version=version_str,
    description='A python library to manage KitOps ModelKits and Kitfiles',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Brett Hodges',
    author_email='brett@jozu.com',
    url='https://github.com/jozu-ai/pykitops',
    license='Apache-2.0 License',
    python_requires='>=3.10.0',
    packages=['kitops'],
    keywords=['kitfile', 'modelkit', 'kitops', 'jozu', 'jozu.ml'],
    install_requires=requirements.pop('base'),
    extras_require=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache-2.0 License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
