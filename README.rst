Running tests with CoverageTestRunner
=====================================

Download missing dependencies (should be already in repository)::

    mkdir libs
    wget http://git.liw.fi/cgi-bin/cgit/cgit.cgi/coverage-test-runner/snapshot/coverage-test-runner-coverage-test-runner-1.11.tar.gz -O libs/CoverageTestRunner-1.11.tar.gz

Install all needed tools and Qvarn into a virtualenv::

    test -f qvarn/requirements.txt
    mkvirtualenv -p /usr/bin/python2.7 qvarn
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
    ../prepare-db.py

Add these two sections to ``~/.config/qvarn/createtoken.conf``::

    [http://127.0.0.1:9090]
    client_id = 
    client_secret = 

    [https://127.0.0.1:9090]
    client_id = 
    client_secret = 

Generate self-signed SSL certificate (this should be already generated)::

    openssl genrsa -out ssl.key 2048
    openssl req -new -key ssl.key -out ssl.csr
    openssl x509 -req -days 365 -in ssl.csr -signkey ssl.key -out ssl.crt

See: http://uwsgi-docs.readthedocs.io/en/latest/HTTPS.html

Run Qvarn instance::

    cd qvarn
    uwsgi --https-socket 127.0.0.1:9090,../ssl.crt,../ssl.key --wsgi-file ../server.py --pyargv '--config ../qvarn.conf' --master --py-autoreload 1

Some tests do not pass with https, as a workaround, you can run tests with
http::

    cd qvarn
    uwsgi --http-socket 127.0.0.1:9090 --wsgi-file ../server.py --pyargv '--config ../qvarn.conf' --master --py-autoreload 1

But for this, you need to fix two files in Qvarn sources, where https is
hardcoded::

    qvarn/list_resource.py:259: ('https',) + urlparse.urlparse(resource_url)[1:])
    qvarn/listener_resource.py:215: ('https',) + urlparse.urlparse(resource_url)[1:])


Finally you run tests using this command::

    ../apitests.py path/to/virtualenv https://127.0.0.1:9090 --stop-on-first-fail

If something fails, you can run tests like this::

    ../apitests.py path/to/virtualenv https://127.0.0.1:9090 -v --stop-on-first-fail -r 'manage a person' --tempdir /tmp/qvarn-test-api --snapshot

This will output more information about test run and also leaves all temporary
files in specified ``--tempdir``.
