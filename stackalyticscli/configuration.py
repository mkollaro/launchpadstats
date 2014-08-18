#!/usr/bin/env python
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
from os.path import dirname, join, normpath

PROJ_DIR = normpath(join(dirname(__file__), ".."))
LOG = logging.getLogger('stackalyticscli')


def get_config(filepath=None):
    """Read the .ini configuration file given in filepath.

    If no filepath is given, try reading 'config.ini' in the stackalytiscli
    project directory.
    :returns: ConfigParser object
    """
    if not filepath:
        filepath = join(PROJ_DIR, 'config.ini')
    LOG.info("Reading configuration file '%s'", filepath)

    config = ConfigParser.ConfigParser()
    config.read(filepath)
    return config
