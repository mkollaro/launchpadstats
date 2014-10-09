#!/usr/bin/env python
#
# Copyright (c) 2014 Martina Kollarova
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
import mock
from nose.tools import raises, assert_equals

from launchpadstats import common
from launchpadstats import tables
import fakes


def fake_request(url, params):
    """Simulate `requests.get()` on the stackalytics API."""
    return fakes.GOOD_RESPONSE


class TestTable(object):
    @raises(common.ConfigurationError)
    def test_empty_query(self):
        tables.GroupMetricsTable(people='', releases='', metrics='')

    @raises(common.ConfigurationError)
    def test_no_releases(self):
        tables.GroupMetricsTable(people='user1', releases='',
                                 metrics='loc')

    @raises(common.ConfigurationError)
    def test_no_people(self):
        tables.GroupMetricsTable(people='', releases='havana',
                                 metrics='loc')

    @raises(common.ConfigurationError)
    def test_no_metrics(self):
        tables.GroupMetricsTable(people='user1', releases='havana',
                                 metrics='')

    @raises(common.ConfigurationError)
    def test_unknown_metric(self):
        tables.GroupMetricsTable(people='user1', releases='havana',
                                 metrics='some-unknown-metric')


class TestGroupMetricsTable(object):
    def setup(self):
        self.patch = \
            mock.patch('launchpadstats.tables.stackalytics.requests.get',
                       side_effect=fake_request)
        self.mock_request = self.patch.start()

    def teardown(self):
        self.patch.stop()

    def test_simple_query(self):
        table = tables.GroupMetricsTable(people='user1', releases='icehouse',
                                         metrics='loc')
        fake_response = fakes.GOOD_RESPONSE.json()['contribution']
        expected_result = [
            (table.header_info, 'icehouse'),
            (common.PRETTY_NAME['loc'], str(fake_response['loc'])),
            ('sum', '0')  # because LOC is in `SKIP_FROM_SUM`
        ]
        table.generate()
        matrix = table.matrix()
        assert_equals(matrix, expected_result)

    def test_query(self):
        table = tables.GroupMetricsTable(people='user1,user2,user3',
                                         releases='havana,icehouse,juno',
                                         metrics='loc')
        fake_loc = str(fakes.GOOD_RESPONSE.json()['contribution']['loc'])
        expected_result = [
            (table.header_info, 'havana', 'icehouse', 'juno'),
            (common.PRETTY_NAME['loc'], fake_loc, fake_loc, fake_loc),
            ('sum', '0', '0', '0')  # because LOC is in `SKIP_FROM_SUM`
        ]
        table.generate()
        assert_equals(table.matrix(), expected_result)

    def test_release_order(self):
        table = tables.GroupMetricsTable(people='user1',
                                         releases='havana,juno,icehouse',
                                         metrics='loc')
        table.generate()
        assert_equals(table.matrix()[0],
                      (table.header_info, 'havana', 'juno', 'icehouse'))

    def test_metrics(self):
        # test all metrics except reviews and sum
        metrics = common.METRICS - set(['reviews'])
        table = tables.GroupMetricsTable(people='user1,user2,user3',
                                         releases='havana',
                                         metrics=','.join(metrics))
        table.generate()
        matrix = table.matrix()
        assert_equals(_matrix_size(matrix), (len(metrics) + 2, 2))
        assert_equals(matrix[0], (table.header_info, 'havana'))
        fake_response = fakes.GOOD_RESPONSE.json()['contribution']
        for index, metric in enumerate(metrics):
            assert_equals(matrix[index + 1][0], metric)
            assert_equals(matrix[index + 1][1], str(fake_response[metric]))
        assert_equals(matrix[-1][0], 'sum')

    def test_reviews(self):
        table = tables.GroupMetricsTable(people='user1,user2,user3',
                                         releases='havana', metrics='reviews')
        table.generate()
        assert_equals(table.matrix()[1][0], common.PRETTY_NAME['reviews'])
        reviews = table.matrix()[1][1].strip('()').split(',')
        assert_equals(len(reviews), len(common.REVIEWS_FORMAT))
        fake_response = fakes.GOOD_RESPONSE.json()['contribution']
        for index, mark in enumerate(common.REVIEWS_FORMAT):
            assert_equals(reviews[index].strip(),
                          str(fake_response['marks'][mark]))

    def test_sum(self):
        # compute sum of metrics in a table that contains them all
        table = tables.GroupMetricsTable(people='user1,user2,user3',
                                         releases='havana',
                                         metrics=','.join(common.METRICS))
        table.generate()
        matrix = table.matrix()
        assert_equals(matrix[-1][0], 'sum')
        fake_response = fakes.GOOD_RESPONSE.json()['contribution']
        tmp_sum = sum([fake_response[x] for x in common.METRICS
                       if x not in common.SKIP_FROM_SUM])
        assert_equals(matrix[-1][1], str(tmp_sum))


def _matrix_size(matrix):
    rows = len(matrix)
    cols = list(map(len, matrix))
    assert len(set(cols)) == 1, "Matrix columns are not of the same length."
    return rows, cols[0]
