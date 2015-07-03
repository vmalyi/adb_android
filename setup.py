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
    name='adb',
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
        'adb',
    ],
    package_dir={'adb':'adb'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    keywords='adb',
    classifiers=[],
    test_suite='tests',
)
