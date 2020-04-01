#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

requires = [
    'mesa'
]

setup(
    name='disease_sim',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requires
)
