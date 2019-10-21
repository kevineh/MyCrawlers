#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name =          'sample',
    version =       '1.0',
    packages =      find_packages(),
    entry_points =  {'scrapy': ['settings = sample.settings']}
)