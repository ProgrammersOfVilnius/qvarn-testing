from __future__ import unicode_literals, print_function
from __future__ import absolute_import

import sys
import yaml
import sqlparse
import codecs

from qvarn.slog import SlogWriter

try:
    # Python 2
    from ConfigParser import RawConfigParser
    PY2 = True
except ImportError:  # pragma: no cover
    from configparser import RawConfigParser  # noqa
    PY2 = False


def text_representer(dumper, data):
    if data.lstrip().startswith('SELECT '):
        data = sqlparse.format(data, reindent=True)
    if '\n' in data:
        return dumper.represent_scalar(
            u'tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar(
        u'tag:yaml.org,2002:str', data, style='')


yaml.add_representer(str, text_representer)
if PY2:
    yaml.add_representer(unicode, text_representer)


def dumps(msg):
    return yaml.dump(msg, indent=2, default_flow_style=False)


def format_log_line(msg):
    exclude = {'msg_type', 'msg_text'}

    if msg['msg_type'] == 'http-request':
        line = '{_timestamp} #{_msg_number}: {msg_type}: {method} {path}'.format(**msg)
        exclude.update(['method', 'path', 'headers', 'url_args'])

    elif msg['msg_type'] == 'http-response':
        line = '{_timestamp} #{_msg_number}: {msg_type}: {status}'.format(**msg)
        exclude.update(['status'])

    elif msg['msg_type'] == 'exception':
        # Usually 'exception' message just repeats the exception that happened in
        # a previous message.
        #
        # TODO: Probably it would be a good idea to check if we've already seen this
        #       exception and only return if we really showed this exception
        #       previously.
        return ''

    else:
        msg.setdefault('msg_text', '')
        line = '{_timestamp} #{_msg_number}: {msg_type}: {msg_text}'.format(**msg)

    data = {
        k: v
        for k, v in msg.items()
        if k not in exclude and not k.startswith('_')
    }
    if data:
        line += '\n  ' + dumps(data).replace('\n', '\n  ')
    if '_traceback' in msg:
        line += '\n' + msg['_traceback']
    return line


class StdoutSlogWriter(SlogWriter):

    def write(self, log_obj):
        line = format_log_line(log_obj)
        if not isinstance(line, str):
            line = line.encode('UTF-8')
        print(line)
        sys.stdout.flush()

    def close(self):
        pass

    def reopen(self):
        pass


class FileSlogWriter(SlogWriter):

    def __init__(self, filename):
        self._log_filename = filename
        self._open()

    def _open(self):
        self._log_file = codecs.open(self._log_filename, 'w', encoding='utf-8')

    def write(self, log_obj):
        line = format_log_line(log_obj)
        if line is not None:
            self._log_file.write(line + '\n')
            self._log_file.flush()

    def close(self):
        self._log_file.close()
        self._log_file = None

    def reopen(self):
        self._log_file.close()
        self._open()
