#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on August, 4th, 2021

@author: Imam Usmani
"""

from setuptools import setup

scripts=['bin/run_api', 'bin/run_client']
install_requires=[
    'flask',
    'flask_restful',
    'requests',
    'Flask-SQLAlchemy',
    'ipython'
    # 'pandas',
    # 'numpy',
    # 'seaborn',
    # 'scipy',
    # 'engineering_notation',
    # 'pyvisa',
    # 'pyvisa-py',
    # 'PySerial',
    # 'pyusb',
    # 'allantools',
    # 'pyvisa-sim'
    ]

setup(name='rpi_jukebox',
        version='0.1',
        description='',
        author='Imam Usmani',
        author_email='imam.usmani@sfr.fr',
        packages=['rpi_jukebox', 'rpi_jukebox.api', 'rpi_jukebox.utils', 'rpi_jukebox.client'],
        install_requires=install_requires,
        include_package_data=True,
        zip_safe=False,
        scripts=scripts
)
