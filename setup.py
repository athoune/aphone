#!/usr/bin/env python

from setuptools import setup

# http://pypi.python.org/pypi?%3Aaction=list_classifiers

setup(name='aphone',
    version='0.0.4',
    package_dir={'': 'src'},
    url='http://github.com/athoune/aphone',
    #scripts=[],
    description="Reading aspell phonetic grammar rules.",
    long_description="""
First step to build phonetic filter in any languages.
""",
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python',
          'Natural Language :: French',
          'Topic :: Text Processing :: Linguistic',
          'Topic :: Text Processing :: Filters',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        ],
    license="GPLv3",
    author="Mathieu Lecarme",
    packages=['aphone'],
    keywords=["phonetic", "aspell"],
    scripts=['bin/aphone'],
    zip_safe=True,
    install_requires=[],
)
