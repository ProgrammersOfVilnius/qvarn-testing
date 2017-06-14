import os
import tempfile

import pkg_resources as pres

from honcho.manager import Manager


def main():
    with tempfile.TemporaryDirectory() as tmpdir:

        def template(path, context):
            content = pres.resource_string('qvarntesting', 'config/%s' % path)
            dest = os.path.join(tmpdir, path)
            print('creating %s' % dest)
            with open(dest, 'w') as f:
                f.write(content.format(**context))
            return dest

        haproxy_cfg = template('haproxy.cfg', {})
        qvarn_conf = template('qvarn.conf', {})

        m = Manager()
        m.add_process('uwsgi', ' '.join([
            'uwsgi',
            '--http-socket 127.0.0.1:9000',
            '--wsgi-file', pres.resource_filename('qvarntesting', 'server.py'),
            '--pyargv "--config %s"' % qvarn_conf,
            '--master',
            '--py-autoreload 1',
        ]))
        m.add_process('haproxy', 'haproxy -f %s -C %s -db' % (
            haproxy_cfg,
            pres.resource_filename('qvarntesting', 'config/certs'),
        ))
        m.loop()
    return m.returncode


if __name__ == "__main__":
    main()
