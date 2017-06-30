from setuptools import setup, find_packages


setup(
    name='qvarn-testing',
    version='0.1.0',
    description=(
        "Set of scripts for testing or using Qvarn in development environment."
    ),
    author='Suomen Tilaajavastuu Oy',
    author_email='tilaajavastuu.hifi@tilaajavastuu.fi',
    packages=find_packages('.'),
    include_package_data=True,
    install_requires=[
        'sqlparse',  # used by qvarntesting/scripts/readlogs.py
        'honcho',    # process management
        'dataset',   # for persisting gluu users
        'webob',


        # Qvarn dependencies
        'qvarn',
        'PyJWT',
        'bottle',
        'psycopg2',
        'pyyaml',
        'uwsgi',
        'uwsgidecorators',
    ],
    entry_points={
        'console_scripts': [
            'qvtestapi = qvarntesting.scripts.apitests:main',
            'qvtestconfigure = qvarntesting.scripts.configure:main',
            'qvtestinitdb = qvarntesting.scripts.initdb:main',
            'qvtestlogs = qvarntesting.scripts.readlogs:main',
            'qvtestserver = qvarntesting.scripts.server:main',
        ]
    },
)
