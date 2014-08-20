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
    """Base class for the table generators.
    """
    # will be shown on the top left corner, change it in specific
    # implementation of the table
    header_info = "column/row"
    # if True, it will flip the rows and columns in the CSV representation
    # (transpose the matrix)
    _flip = False

    def __init__(self, people, releases, metrics, **kwargs):
        """Set filters for the queries.

        :param people: list or comma-separated string with list of user ids in
            stackalytics
        :param releases: list or comma-separated string with list of OpenStack
            releases that will be passed as the 'release' parameter to the
            query
        :param metrics: which metrics to show in the CSV table (and in some
            cases, create a sum total of them)
        """
        self.people = _split(people)
        self.releases = _split(releases)
        self.metrics = _split(metrics)
        self._data = dict()

    def generate(self):
        """Do a set of queries on stackalysis and save the data.

        The queries depend on what kind of table we need to generate.
        The result should be saved in `self._data`.
        """
        raise NotImplementedError("Method 'generate' is abstract")

    def json(self):
        """Return the JSON raw data, with all the metrics"""
        return self._data

    def csv(self):
        """Return a string with a CSV representation of the data.

        The first item on the top left is going to be the `self.header_info`
        with the description of what the columns and rows are.
        If `self._flip` is True, flip the table (transpose it), i.e. swap the
        columns and the rows.
        """
        # header (or first collumn if it gets flipped)
        header = self._data.keys()
        row = [self.header_info] + header
        result = [row]
        # print data
        for metric in self.metrics + ['sum']:
            row = [metric]
            for item in header:
                row.append(str(self._data[item][metric]))
            result.append(row)
        if self._flip:
            # transpose the matrix
            result = zip(*result)
        result_str = '\n'.join([', '.join(row) for row in result])
        return result_str

    def _add_metrics_sum(self):
        """Add up the fields in 'self.metrics'.

        The result should be saved in the `self._data[item]['sum']`. It will be
        printed in the CSV representation."""
        for key, metrics in self._data.iteritems():
            total = 0
            for metric, value in metrics.iteritems():
                if metric in self.metrics:
                    total += value
            self._data[key]['sum'] = total


class GroupMetricsTable(Table):
    """Show the metrics of the group per release in columns.

    The 'group' is defined as the list of people passed in the 'people'
    parameter. One metric per line is shown, releases are columns. Shows a sum
    of the metrics per release.
    """
    header_info = 'metric/release'

    def generate(self):
        for release in self.releases:
            params = {'release': release, 'user_id': ','.join(self.people)}
            stats = get_stats(params)
            self._data[release] = stats['contribution']
        self._add_metrics_sum()
        LOG.info(json.dumps(self._data, indent=4))


class UserMetricsTable(Table):
    """Show metrics of each user on a separate line.

    For each person in the 'people' parameter, display a line with their
    metrics (given in the 'metrics' param), summed up in all the releases
    specified in the 'releases' param. At the end of the line, show a sum of
    the metrics
    """
    header_info = "user/metric"
    _flip = True

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