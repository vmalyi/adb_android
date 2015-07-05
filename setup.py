#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [
]

test_requirements = [
]

setup(
    name='adb_android',
    version='0.1.0',
    description="Enables android adb in your python script",
    long_description='This package can be used by everyone who implements some \
    android-related stuff on Python and at the same time has to interact with \
    android adb. It makes interaction with android adb easier because of proper \
    error handling and some useful features.',
    author='Viktor Malyi',
    author_email='v.stratus@gmail.com',
    url='https://github.com/vmalyi/adb',
    packages=[
        'adb_android',
    ],
    package_dir={'adb_android':'adb_android'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU",
    keywords='adb, android',
    #TODO: check compatibitily with >2.7
    classifiers=[
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Topic :: Software Development :: Testing',
    'Intended Audience :: Developers'
    ],
    test_suite='tests',
)
