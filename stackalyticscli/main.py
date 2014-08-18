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

import requests
import json
import logging

from stackalyticscli.configuration import get_config

LOG = logging.getLogger('stackalyticscli')


URL = 'http://stackalytics.com/api/1.0/'


def get_stats(config):
    params = dict(config.items('DEFAULT'))

    r = requests.get(URL + 'contribution', params=params)
    LOG.info(r.url)
    return r.json()


def main():
    config = get_config()
    stats = get_stats(config)
    print json.dumps(stats, indent=4)


if __name__ == '__main__':
    main()
