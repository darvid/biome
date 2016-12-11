#!/usr/bin/env python
"""Provides painless access to namespaced environment variables.

Links
-----

* `Source code <http://github.com/darvid/biome>`_
* `Documentation <http://biome.readthedocs.org>`_

"""
import io
import sys

import setuptools


__all__ = ('setup',)


def readme():
    with io.open('README.rst') as fp:
        return fp.read()


def setup():
    """Package setup entrypoint."""
    install_requirements = ["attrdict"]
    if sys.version_info[:2] < (3, 4):
        install_requirements.append("pathlib")
    setup_requirements = ['six', 'setuptools>=17.1', 'setuptools_scm']
    needs_sphinx = {
        'build_sphinx',
        'docs',
        'upload_docs',
    }.intersection(sys.argv)
    if needs_sphinx:
        setup_requirements.append('sphinx')
    setuptools.setup(
        author="David Gidwani",
        author_email="david.gidwani@gmail.com",
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
        description="Painless access to namespaced environment variables",
        download_url="https://github.com/darvid/biome/tarball/0.1",
        install_requires=install_requirements,
        keywords="conf config configuration environment",
        license="BSD",
        long_description=readme(),
        name="biome",
        package_dir={'': 'src'},
        packages=setuptools.find_packages('./src'),
        setup_requires=setup_requirements,
        tests_require=["pytest"],
        url="https://github.com/darvid/biome",
        use_scm_version=True,
    )


if __name__ == '__main__':
    setup()
