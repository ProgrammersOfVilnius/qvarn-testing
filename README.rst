Running tests with CoverageTestRunner
=====================================

Get the version of Qvarn you want to test into a sibling directory named
``qvarn``, e.g. ::

    git clone git://git.qvarnlabs.net/qvarn

Install all needed tools and Qvarn itself into a virtualenv::

    cd qvarn
    mkvirtualenv -p /usr/bin/python2.7 qvarn
    pip install -r ../qvarn-testing/requirements.txt
    pip install -r requirements.txt --find-links ../qvarn-testing/libs
    pip install -e .
    ./check


For Python 3 (for which you need a Python 3 enabled branch of Qvarn from
https://github.com/vaultit/qvarn)::

    cd qvarn
    mkvirtualenv -p /usr/bin/python3.4 qvarn-py3
    pip install -r ../qvarn-testing/requirements.txt
    pip install -r requirements-py3.txt --find-links ../qvarn-testing/libs
    pip install -e .
    ./check


Note that pylint will fail if you run the check script in a Python 2.7
virtualenv on code from the Python 3 branch due to our compatibility shims.


Running tests with py.test
==========================

First install dependencies::

    pip install coverage pytest pytest-cov

Then you can run the tests::

    cd qvarn
    py.test \
      -vvx \
      --tb=native \
      -c ../qvarn-testing/pytest.ini \
      --cov-config=../qvarn-testing/pytest.ini \
      --cov-report=term-missing \
      qvarn

Note: this doesn't work for me (py.test fails to recognize --cov-* options),
and I've no clue why!


Running integration tests
=========================

Install the tools::

    cd qvarn-testing
    mkvirtualenv -p /usr/bin/python2.7 qvarn-testing
    pip install -r requirements-integration.txt
    pip install cliapp --find-links libs
    pip install ttystatus --find-links libs
    pip install cmdtest --find-links libs
    pip install -e ../qvarn
    pip install -e .


Create Postgresql database user and database::

    > sudo -u postgres createuser $USER
    > sudo -u postgres createdb qvarn -O $USER

Then initialize the Qvarn database::

    qvtestinitdb ../qvarn/resource_type

This will create several configuration files under ``/tmp/qvtest``.

Generate self-signed SSL certificate::

    openssl genrsa -out ssl.key 2048
    openssl req -new -key ssl.key -out ssl.csr
    openssl x509 -req -days 365 -in ssl.csr -signkey ssl.key -out ssl.crt
    cat ssl.crt ssl.key > ssl.pem

See: http://uwsgi-docs.readthedocs.io/en/latest/HTTPS.html
     https://help.ubuntu.com/lts/serverguide/certificates-and-security.html
     http://stackoverflow.com/a/991772/475477

Run Qvarn instance and Haproxy::

    workon qvarn-py3
    pip install -e .
    qvtestserver ../qvarn/resource_type

Finally you can run tests using this command::

    export QVARN_CREATETOKEN_CONF=$PWD/createtoken.conf
    cd qvarn
    qvtestapi /tmp/qvtest/etc/qvarn.conf --stop-on-first-fail

If something fails, you can run tests like this::

    qvtestapi /tmp/qvtest/etc/qvarn.conf -v --stop-on-first-fail -r 'manage a person' --snapshot

This will output more information about test run and also leaves all temporary
test files in a snapshot directory.

After running tests one time, in order to run tests again, first you need to
clean database, because tests leaves test data in database and will fail if you
try to run them again. To clean database, run this command::

    sudo -u postgres psql qvarn -f drop_everything.sql
    qvtestinitdb ../qvarn/resource_type

Do not forget to turn off uwsgi first (with a Ctrl+C), to unlock database
resource for dropping.


How to use real Gluu server?
----------------------------

In order to use real Gluu server you need to modify
``/tmp/qvtest/etc/haproxy.cfg``::

  frontend http-in
      bind *:9080
      bind *:9443 ssl crt ssl.pem
      default_backend qvarn

      acl resource_auth path_beg /auth
      use_backend gluu if resource_auth

  backend gluu
      server gluu bolagsfakta-gluu-dev.pov.lt:443 ssl verify none
      option forwardfor
      acl gluu_rewrite path_beg /auth
      reqrep ^(.*)\ /auth/(.*)$ \1\ /oxauth/seam/resource/restv1/oxauth/\2 if gluu_rewrite
      reqadd X-Forwarded-Proto:\ https


Debugging integration tests
---------------------------

When running qvarn with ``qvtestserver`` all logs will be written to stdout
and to ``/tmp/qvarn.log``. If you want to print something there, you need to
print it this way::

    qvarn.log.log('debug', msg_text='Your message', key1=v1, key2=v2)

And this will be visible in the output. ``key1=v1, key2=v2`` are optional
keyword argument, that will be printed too if provided.


How to read and write yarn test files
=====================================

Here are some useful resources:

- http://blog.liw.fi/posts/yarn/

- http://liw.fi/cmdtest/
