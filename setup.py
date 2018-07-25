#!/usr/bin/env python
"""Package metadata for logcrm_event_bus."""


from setuptools import setup

setup(
    name='logcrm_event_bus',
    packages=['logcrm_event_bus'],
    include_package_data=True,
    install_requires=[
        'moflask',
        'celery[redis]',
        'mohawk',
        'raven[flask]',
        'requests~=2.19',
    ],
    dependency_links=[
        'git+https://github.com/moreonion/moflask.git'
        '@614602c801fe53d616e7fb14cfbcc98ec3ad31cf#egg=moflask'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
