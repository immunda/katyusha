# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="katyusha",
    version="0.0.1",
    author="Phil Howell",
    author_email="phil@quae.co.uk",
    description="Simple helpers for building RESTful APIs with Flask and MongoEngine",
    license="BSD",
    install_requires=required,
    keywords="flask api rest mongo mongoengine restful",
    url="https://github.com/immunda/katyusha",
    packages=['katyusha', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
