Running tests with CoverageTestRunner
=====================================

Download missing dependencies (should be already in repository)::

    mkdir libs
    wget http://git.liw.fi/cgi-bin/cgit/cgit.cgi/coverage-test-runner/snapshot/coverage-test-runner-coverage-test-runner-1.11.tar.gz -O libs/CoverageTestRunner-1.11.tar.gz

Install all needed tools and Qvarn into a virtualenv::

    test -f qvarn/requirements.txt
    mkvirtualenv -p /usr/bin/python2.7 qvarn
    pip install -r requirements.txt
    cd qvarn
    pip install coverage
    pip install -r requirements.txt --find-links ../libs
    pip install psycopg2
    pip install uwsgidecorators
    pip install -e .
    ./check


Running tests with py.test
==========================

First install needed dependencies::

    pip install coverage pytest pytest-cov

Then create ``pytest.ini`` file::

    [pytest]
    python_files=*_tests.py

Then you can run tests:

::

    py.test -vvx --tb=native --cov-config=../pytest.ini --cov-report=term-missing --cov=qvarn qvarn


Running integration tests
=========================

First download the tools (these should be already downloaded and added to the
repository)::

    cd libs
    wget http://git.liw.fi/cgi-bin/cgit/cgit.cgi/ttystatus/snapshot/ttystatus-0.32.tar.gz
    wget http://git.liw.fi/cgi-bin/cgit/cgit.cgi/cliapp/snapshot/cliapp-1.20160724.tar.gz
    wget http://git.liw.fi/cgi-bin/cgit/cgit.cgi/cmdtest/snapshot/cmdtest-0.27.tar.gz

Then install the tools::

    cd ..
    pip install markdown pyyaml
    pip install cmdtest --find-links libs
    pip install ttystatus --find-links libs
    pip install cliapp --find-links libs


Create database user and database::

    > sudo -u postgres psql                                                      
    postgres=# CREATE USER qvarn WITH PASSWORD 'secret';
    postgres=# CREATE DATABASE qvarn;
    postgres=# GRANT ALL PRIVILEGES ON DATABASE qvarn TO qvarn;


Then initialize Qvarn database (see ``qvarn.conf``)::

    cd qvarn
    ../initdb.py

Add these two sections to ``~/.config/qvarn/createtoken.conf``::

    [http://127.0.0.1:9080]
    client_id = 
    client_secret = 

    [https://127.0.0.1:9443]
    client_id = 
    client_secret = 

Generate self-signed SSL certificate (this should be already generated)::

    openssl genrsa -out ssl.key 2048
    openssl req -new -key ssl.key -out ssl.csr
    openssl x509 -req -days 365 -in ssl.csr -signkey ssl.key -out ssl.crt
    cat ssl.crt ssl.key > ssl.pem

See: http://uwsgi-docs.readthedocs.io/en/latest/HTTPS.html
     https://help.ubuntu.com/lts/serverguide/certificates-and-security.html
     http://stackoverflow.com/a/991772/475477

Run Qvarn instance and Haproxy::

    cd qvarn
    uwsgi --http-socket 127.0.0.1:9000 --wsgi-file ../server.py --pyargv '--config ../qvarn.conf' --master --py-autoreload 1
    haproxy -f haproxy.cfg -C .. -db

Finally you can run tests using this command::

    ../apitests.py ../qvarn.conf --stop-on-first-fail

If something fails, you can run tests like this::

    ../apitests.py ../qvarn.conf -v --stop-on-first-fail -r 'manage a person' --snapshot

This will output more information about test run and also leaves all temporary
test files in a snapshot directory.

After running tests one time, in order to run tests again, first you need to
clean database, because tests leaves test data in database and will fail if you
try to run them again. To clean database, run this command::

    dropdb qvarn && createdb qvarn && ../initdb.py

Do not forget to turn off uwsgi, to unlock database resource for dropping.


Debugging integration tests
---------------------------

When running integrations tests using ``../apitests.py`` on error you will get
last error with whole context. If you want to print something there, you need
to print it this way::

    qvarn.log.log('debug', msg_text='Your message', key1=v1, key2=v2)

And this will be visible in the output. ``key1=v1, key2=v2`` are optional
keyword argument, that will be printed too if provided.


How to read and write yarn test files
=====================================

Here are some usefull resources:

- http://blog.liw.fi/posts/yarn/

- http://liw.fi/cmdtest/
