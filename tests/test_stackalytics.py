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
import requests
from nose.tools import raises, assert_equals

import launchpadstats.stackalytics
import fakes


def fake_request(method, url, params=None, *args, **kwargs):
    """Simulate `requests.sessions.Session.request()` on the stackalytics API.
    """
    if 'user_id' not in params:
        return fakes.GOOD_RESPONSE
    elif params['user_id'].startswith('known_user'):
        return fakes.GOOD_RESPONSE
    else:
        return fakes.BAD_RESPONSE


class TestStat():
    @mock.patch('launchpadstats.stackalytics.requests.get')
    def test_empty_params(self, fake_request):
        fake_request.return_value = fakes.GOOD_RESPONSE
        res = launchpadstats.stackalytics.get_stats(dict())
        assert_equals(res, fakes.GOOD_RESPONSE.json())

    @mock.patch('launchpadstats.stackalytics.requests.get')
    @raises(requests.HTTPError)
    def test_bad_response(self, fake_request):
        fake_request.return_value = fakes.BAD_RESPONSE
        launchpadstats.stackalytics.get_stats({'something_bad': ''})


class TestUsers():
    def setup(self):
        self.patch = \
            mock.patch('launchpadstats.stackalytics'
                       '.requests_futures.sessions.Session.request',
                       side_effect=fake_request)
        self.mock_request = self.patch.start()

    def teardown(self):
        self.patch.stop()

    def test_user_exists(self):
        users = ['known_user1']
        res = launchpadstats.stackalytics.get_registered_users(users)
        assert_equals(res, users)

    def test_user_doesnt_exist(self):
        users = ['unknown_user1']
        res = launchpadstats.stackalytics.get_registered_users(users)
        assert_equals(res, list())

    def test_multiple_users_check(self):
        users = ['unknown_user1', 'known_user2']
        res = launchpadstats.stackalytics.get_registered_users(users)
        assert_equals(res, ['known_user2'])

    def test_empty_user_list(self):
        res = launchpadstats.stackalytics.get_registered_users([])
        assert_equals(res, list())
