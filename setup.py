#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='project',
    version='0.0.1',
    description='Course project for ECS 260',
    author='Kunal Mundada',
    author_email='',
    # REPLACE WITH YOUR OWN GITHUB PROJECT LINK
    url='https://github.com/AlKun25/ECS_260',
    install_requires=['pydriller','PyGithub','python-dotenv'],
    packages=find_packages(),
)

