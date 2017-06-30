from __future__ import unicode_literals
from __future__ import absolute_import

import argparse
import logging

from qvarntesting.logs import set_up_logging
from qvarntesting.configs import create_config_files
from qvarntesting.constants import DEFAULT_BASE_DIR

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--basedir', default=DEFAULT_BASE_DIR, help="path to config files and etc.")
    args = parser.parse_args()

    set_up_logging()
    create_config_files(args.basedir)


if __name__ == "__main__":
    main()
