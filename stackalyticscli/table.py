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


import logging
import json

from stackalyticscli import get_stats

LOG = logging.getLogger('stackalyticscli')


class Table(object):
    header_info = ""
    _flipped = False

    def __init__(self, people, releases, metrics, **kwargs):
        self.people = _split(people)
        self.releases = _split(releases)
        self.metrics = _split(metrics)
        self._data = dict()

    def generate(self):
        raise NotImplementedError("Method 'generate' is abstract")

    def _add_metrics_sum(self):
        """Add up the fields in 'self.metrics' and save them under 'sum'"""
        for key, metrics in self._data.iteritems():
            total = 0
            for metric, value in metrics.iteritems():
                if metric in self.metrics:
                    total += value
            self._data[key]['sum'] = total

    def json(self):
        return self._data

    def csv(self):
        # print header
        result = self.header_info + ', '
        header = self._data.keys()
        result += ', '.join(header) + '\n'
        # print data
        for metric in self.metrics + ['sum']:
            line = [metric]
            for item in header:
                line.append(str(self._data[item][metric]))
            result += ', '.join(line) + '\n'
        return result


class GroupMetricsTable(Table):
    header_info = 'metric/release'

    def generate(self):
        for release in self.releases:
            params = {'release': release, 'user_id': ','.join(self.people)}
            stats = get_stats(params)
            self._data[release] = stats['contribution']
        self._add_metrics_sum()
        LOG.info(json.dumps(self._data, indent=4))


class UserMetricsTable(Table):
    header_info = "user/metric"
    _flipped = True

    def generate(self):
        for person in self.people:
            params = {'release': ','.join(self.releases), 'user_id': person}
            stats = get_stats(params)
            self._data[person] = stats['contribution']
        self._add_metrics_sum()
        LOG.info(json.dumps(self._data, indent=4))


def _split(maybe_string):
    """If it's a string, split it by the comma char, otherwise just return"""
    if isinstance(maybe_string, basestring):
        return maybe_string.split(',')
    else:
        return maybe_string
