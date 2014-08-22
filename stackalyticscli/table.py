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


import logging
import json
import abc

from stackalyticscli import get_stats

LOG = logging.getLogger('stackalyticscli')

# characters used as separator between items in the CSV output
CSV_SEPARATOR = '; '
# which metrics should be skipped when a sum is made of the metrics
SKIP_FROM_SUM = ['marks', 'loc']


class Table(object):
    """Base class for the table generators.
    """
    __metaclass__ = abc.ABCMeta

    # will be shown on the top left corner, change it in specific
    # implementation of the table
    header_info = "column/row"
    # if True, it will flip the rows and columns in the CSV representation
    # (transpose the matrix)
    _flip = False
    # show the total of the data at the end of the table
    _show_sum = False

    def __init__(self, people, releases, metrics, **kwargs):
        """Set filters for the queries.

        :param people: comma-separated string with list of user ids in
            stackalytics
        :param releases: comma-separated string with list of OpenStack
            releases that will be passed as the 'release' parameter to the
            query
        :param metrics: comma-separated string with list of metrics to show in
            the CSV table (and in some cases, create a sum total of them)
        """
        self.people = people.split(',')
        self.releases = releases.split(',')
        self.metrics = metrics.split(',')
        self._data = dict()
        self._data_matrix = list()

    @abc.abstractmethod
    def generate(self):
        """Do a set of queries on stackalysis and save the data.

        The queries depend on what kind of table we need to generate.
        The result should be saved in `self._data`.
        """
        pass

    def json(self):
        """Return the JSON raw data, with all the metrics"""
        return self._data

    def csv(self, delimiter=CSV_SEPARATOR):
        """Return a string with a CSV representation of the data.

        The first item on the top left is going to be the `self.header_info`
        with the description of what the columns and rows are.
        If `self._flip` is True, flip the table (transpose it), i.e. swap the
        columns and the rows.
        :param delimiter: use to separate items
        """
        return '\n'.join([delimiter.join(line) for line in self._data_matrix])

    def _parse_data(self):
        self._add_metrics_sum()
        LOG.info(json.dumps(self._data, indent=4))
        # header (or first collumn if it gets flipped)
        header = self._data.keys()
        row = [self.header_info] + header
        result = [row]
        # print data
        for metric in self.metrics + ['sum']:
            if metric == 'sum' and not self._show_sum:
                # don't show the sum if it's not in the data
                continue
            row = [self._prettify_metric(metric)]
            for item in header:
                row.append(self._prettify_data(self._data[item], metric))
            result.append(row)

        if self._flip:
            # transpose the matrix
            result = zip(*result)
        self._data_matrix = result

    def _add_metrics_sum(self):
        """Add up the fields in `self.metrics`.

        Skip the items in `SKIP_FROM_SUM` even if they are given in
        `self.metrics`, e.g. the review marks.
        The result should be saved in the `self._data[item]['sum']`. It will be
        printed in the CSV representation."""
        for key, metrics in self._data.iteritems():
            total = 0
            for metric, value in metrics.iteritems():
                if metric in self.metrics and metric not in SKIP_FROM_SUM:
                    total += value
            self._data[key]['sum'] = total

    def _prettify_metric(self, metric):
        """Change the names of some metrics to something more readable.
        """
        if metric == 'reviews':
            return 'reviews (-2, -1, +1, +2, A)'
        else:
            return metric

    def _prettify_data(self, data, metric):
        """Change some data (e.g. review marks) into something more readable.
        """
        if metric == 'reviews':
            marks = data['marks']
            result = [str(marks[i]) for i in ['-2', '-1', '1', '2', 'A']]
            result = '(' + ', '.join(result) + ')'
        else:
            result = str(data[metric])
        return result


class GroupMetricsTable(Table):
    """Show the metrics of the group per release in columns.

    The 'group' is defined as the list of people passed in the 'people'
    parameter. One metric per line is shown, releases are columns. Shows a sum
    of the metrics per release.
    """
    header_info = 'metric/release'
    _show_sum = True

    def generate(self):
        for release in self.releases:
            params = {'release': release, 'user_id': ','.join(self.people)}
            stats = get_stats(params)
            self._data[release] = stats['contribution']
        self._parse_data()


class UserMetricsTable(Table):
    """Show metrics of each user on a separate line.

    For each person in the 'people' parameter, display a line with their
    metrics (given in the 'metrics' param), summed up in all the releases
    specified in the 'releases' param.
    """
    header_info = "user/metric"
    _flip = True

    def generate(self):
        for person in self.people:
            params = {'release': ','.join(self.releases), 'user_id': person}
            stats = get_stats(params)
            self._data[person] = stats['contribution']
        self._parse_data()
