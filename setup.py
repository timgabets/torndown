#!/usr/bin/env python
from setuptools import setup

version = '0.0.1'

classifiers = ["Development Status :: 1 - Planning",
               "License :: OSI Approved :: Apache Software License",
               "Programming Language :: Python",
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: 3.2",
               "Programming Language :: Python :: 3.3",
               "Programming Language :: Python :: Implementation :: PyPy"]

with open('requirements.txt') as f:
    install_requires = f.readlines()

setup(name='torndown',
      version=version,
      description="(Tornado + Markdown) Markdown w/ Github integration",
      long_description="""Tornado web plugin to generate pages from Markdown.
                          Markdown may be stored in a foreign repository for
                          high flexability and control.""",
      classifiers=classifiers,
      keywords="tornado markdown web server github",
      author='@timgabets',
      author_email='tim@gabets.ru',
      url='http://github.com/timgabets/torndown',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=['torndown'],
      include_package_data=True,
      zip_safe=True,
      install_requires=install_requires,
      entry_points=None)
