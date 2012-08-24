"""Setuptools setup file"""

import sys
import os
import logging

from setuptools import setup

# Ridiculous as it may seem, we need to import multiprocessing and logging here
# in order to get tests to pass smoothly on python 2.7.
try:
    import multiprocessing
    import logging
except:
    pass

def get_description():
    # TODO -- open README.rst
    return ""

requires = [
    'daemon',
]

setup(
    name='mattd.core',
    version='0.0.1',
    description="Voice-driven scriptable daemon.  Matt Daemon.",
    long_description = get_description(),
    install_requires=requires,
    url = "http://mattd.rtfd.org/",
    author='Ralph Bean',
    author_email='rbean@redhat.com',
    license='AGPLv3+',
    packages = ['mattd', 'mattd.core', 'mattd.plugins',],
    namespace_packages = ['mattd', 'mattd.plugins',],
    include_package_data=True,
    zip_safe=False,
    entry_points="""
    [console_scripts]
    mattd = mattd.core.app:main
    """

)
