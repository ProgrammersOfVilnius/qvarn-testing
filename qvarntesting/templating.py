from __future__ import unicode_literals
from __future__ import absolute_import

from jinja2 import Environment, PackageLoader, select_autoescape


def render(name, context):
    env = Environment(
        loader=PackageLoader('qvarntesting', 'templates'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template(name)
    return [template.render(**context).encode('utf-8')]
