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


from __future__ import absolute_import, print_function, unicode_literals
import logging
import json
import abc
from collections import defaultdict
try:
    from collections import OrderedDict
except ImportError:  # Python 2.6
    from odict import odict as OrderedDict

from launchpadstats import stackalytics
from launchpadstats import common

LOG = logging.getLogger('launchpadstats')


class Table(object):
    """Base class for the table generators.

    The main data are held in 2 structures:
        `self._data` is a order dictionary of dictionaries. The first level of
                     keys depends on the subclass - e.g. releases in
                     group-metrics and users in user-metrics. The second level
                     might not be ordered and should be the individual metrics,
                     e.g. 'loc', 'commit_count', etc.
        `self._data_matrix` is a 2D array (list of tuples) that contains the
                    same data in their almost final form - to be converted
                    into CSV or HTML
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

    def __init__(self, people, releases, metrics, company='',
                 project_type='all', **kwargs):
        """Set filters for the queries.

        :param people: comma-separated string with list of user IDs in
            the stackalytics web page
        :param releases: comma-separated string with list of OpenStack
            releases that will be passed as the 'release' parameter to the
            query
        :param metrics: comma-separated string with list of metrics to show in
            the CSV table (and in some cases, create a sum total of them)
        """
        # The default parameters to the requests, to be overwritten by the
        # `self.generate()` method depending on what request is needed
        self._request_params = {
            'user_id': people,
            'release': releases,
            'company': company,
            'project_type': project_type,
        }
        self.people = _split_and_check(people, "people")
        self.releases = _split_and_check(releases, "releases")
        self.metrics = _split_and_check(metrics, "metrics")
        unknown_metrics = set(self.metrics) - common.METRICS
        if unknown_metrics:
            raise common.ConfigurationError("Metrics '%s' are not supported." %
                                            unknown_metrics)
        self._data = OrderedDict()
        self._data_matrix = list()

    @abc.abstractmethod
    def generate(self):
        """Do a set of queries on stackalysis and save the data.

        If `self._flip` is True, the matrix of data will be flipped
        (transposed), i.e. the the columns and rows will be swapped.

        The queries depend on what kind of table we need to generate.
        The result should be saved in `self._data`.
        """
        pass

    def matrix(self):
        return self._data_matrix

    def csv(self, delimiter=common.CSV_SEPARATOR):
        """Return a string with a CSV representation of the data.

        The first item on the top left is going to be the `self.header_info`
        with the description of what the columns and rows are.

        :param delimiter: use to separate items
        """
        return '\n'.join([delimiter.join(line) for line in self._data_matrix])

    def html(self):
        """Return a string with an HTML representation of the data.

        The first item on the top left is going to be the `self.header_info`
        with the description of what the columns and rows are.
        """
        return _get_html_table(self._data_matrix)

    def _parse_data(self):
        self._add_metrics_sum()
        LOG.info(json.dumps(self._data, indent=4))
        # header (or first collumn if it gets flipped)
        header = tuple(self._data.keys())
        row = (self.header_info,) + header
        result = [row]
        # print data
        for metric in self.metrics + ['sum']:
            if metric == 'sum' and not self._show_sum:
                # don't show the sum if it's not in the data
                continue
            row = [common.PRETTY_NAME[metric]]
            for item in header:
                row.append(self._prettify_data(self._data[item], metric))
            result.append(tuple(row))

        if self._flip:
            # transpose the matrix
            result = list(zip(*result))
        self._data_matrix = result

    def _add_metrics_sum(self):
        """Add up the fields in `self.metrics`.

        Skip the items in `SKIP_FROM_SUM` even if they are given in
        `self.metrics`, e.g. the review marks.
        The result should be saved in the `self._data[item]['sum']`. It will be
        printed in the CSV representation.
        """
        for key in list(self._data.keys()):
            total = 0
            for metric in self.metrics:
                if metric not in common.SKIP_FROM_SUM:
                    total += self._data[key][metric]
            self._data[key]['sum'] = total

    def _prettify_data(self, data, metric):
        """Change some data (e.g. review marks) into something more readable.
        """
        if metric == 'reviews':
            marks = data['marks']
            result = [str(marks[i]) for i in common.REVIEWS_FORMAT]
            return '(' + ', '.join(result) + ')'
        if metric not in data or data[metric] is None:
            return ''
        else:
            return str(data[metric])


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
            self._request_params['release'] = release
            stats = stackalytics.get_stats(self._request_params)
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
        user_exists = stackalytics.check_users_exist(self.people)
        for person in self.people:
            self._data[person] = defaultdict(None)
            if user_exists[person]:
                self._request_params['user_id'] = person
                r = stackalytics.get_stats(self._request_params)
                stats = defaultdict(None, r['contribution'])
                self._data[person] = stats
        self._parse_data()

    def html(self):
        """Generate HTML representation and add links to users."""
        new_matrix = [self._data_matrix[0]]
        for row in self._data_matrix[1:]:
            row = list(row)
            user = row[0]
            row[0] = '<a href=%s?user_id=%s&release=%s>%s</a>' \
                     % (stackalytics.STACKALYTICS_URL,
                        user, ','.join(self.releases), user)
            new_matrix.append(row)
        return _get_html_table(new_matrix)


def get_table(table_type, params):
    """Return the correct Table subclass based on table_type.

    :param table_type: name of one of the implemented Table subclasses, e.g.
        'group-metrics', 'user-metrics'. The 'group-metrics' type will be used
        as default, if None is passed.
    :param params: dictionary of parameters that will be passed to the init
        method of the Table subclass
    """
    if table_type == 'group-metrics' or table_type is None:
        return GroupMetricsTable(**params)
    elif table_type == 'user-metrics':
        return UserMetricsTable(**params)
    else:
        raise Exception("Unknown table type '%s'" % table_type)


def _get_html_table(matrix):
    result = '<table>\n'
    for row in matrix:
        result += '<tr>\n    <td>'
        result += '</td>\n    <td>'.join(row)
        result += '</td>\n</tr>\n'
    result += '</table>'
    return result


def _split_and_check(list_in_string, name):
    if not list_in_string:
        raise common.ConfigurationError("No %s provided" % name)

    result = [x.strip() for x in list_in_string.split(',')]
    if '' in result:
        raise common.ConfigurationError("Empty item in the %s list" % name)
    return result
