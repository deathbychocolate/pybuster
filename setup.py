#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="pybuster",
    packages=find_packages(exclude=["*tests*"]),
    install_requires=["requests", "mypy", "validators", "types-requests", "fake-useragent"],
    entry_points={"console_scripts": ["pybuster=pybuster.main:main"]},
)
