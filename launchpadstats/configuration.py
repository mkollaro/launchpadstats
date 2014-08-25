# Copyright (c) 2014 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Read the configuration file."""

import logging
import ConfigParser
from os.path import isfile

LOG = logging.getLogger('launchpadstats')

DEFAULTS = {
    'project_type': 'all',
    'company': '',
    'people': 'all',
    'releases': 'all',
    'table_type': 'group-metrics',
    'metrics': 'filed_bug_count,resolved_bug_count',
}


def get_config(filepath):
    """Read the .ini configuration file given in filepath.

    If no filepath is given, try reading 'config.ini' in the project directory.

    :returns: ConfigParser object
    """
    LOG.info("Reading configuration file '%s'", filepath)
    if not isfile(filepath):
        raise Exception("No such file '%s'" % filepath)

    config = ConfigParser.ConfigParser(DEFAULTS)
    config.read(filepath)
    return config
