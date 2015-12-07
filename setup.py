#!/usr/bin/env python
"""
    biome
    ~~~~~
    Provides painless access to namespaced environment variables.

    Links
    -----

    * `Source code <http://github.com/darvid/biome>`_
    * `Documentation <http://biome.readthedocs.org>`_
"""
import sys

from setuptools import setup


install_requires = ["orderedattrdict"]
if sys.version_info[:2] < (3, 4):
    install_requires.append("pathlib")


setup(
    name="biome",
    version="0.1",
    description="Painless access to namespaced environment variables",
    license="BSD",
    author="David Gidwani",
    author_email="david.gidwani@gmail.com",
    url="https://github.com/darvid/biome",
    download_url="https://github.com/darvid/biome/tarball/0.1",
    keywords="conf config configuration environment",
    py_modules=["biome"],
    install_requires=install_requires,
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
