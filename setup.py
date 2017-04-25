from setuptools import setup, find_packages

qvarn_version = '0.78'

setup(
    name='qvarntesting',
    version=qvarn_version,
    description='Tilaajavastuu Bolagsfakta Application',
    author='Suomen Tilaajavastuu Oy',
    author_email='tilaajavastuu.hifi@tilaajavastuu.fi',
    packages=find_packages('.'),
    include_package_data=True,
    install_requires=[
        'sqlparse',  # used by qvarntesting/scripts/readlogs.py
        'honcho',

        # Qvarn dependencies
        'PyJWT',
        'bottle',
        'psycopg2',
        'pyyaml',
        'uwsgi',
        'uwsgidecorators',
    ],
    dependency_links=[
        'https://github.com/qvarn/qvarn/archive/qvarn-{0}.tar.gz#egg=qvarn-{0}'.format(qvarn_version),
    ],
    entry_points={
        'console_scripts': [
            'qvtestapi = qvarntesting.scripts.apitests:main',
            'qvtestinitdb = qvarntesting.scripts.initdb:main',
            'qvtestlogs = qvarntesting.scripts.readlogs:main',
            'qvtestserver = qvarntesting.scripts.server:main',
        ]
    },
)
