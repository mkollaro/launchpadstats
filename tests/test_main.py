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
import nose.tools

import launchpadstats.stackalytics
import fakes


class TestStats():
    def setup(self):
        self.good_response = fakes.response(content=fakes.CONTRIBUTION_STATS)
        self.bad_response = fakes.response(status_code=404, reason="Not Found")

    @mock.patch('launchpadstats.stackalytics.requests')
    def test_empty_params(self, mock_requests):
        mock_requests.get.return_value = self.good_response
        r = launchpadstats.stackalytics.get_stats(dict())
        nose.tools.assert_equals(r, self.good_response.json())

    @nose.tools.raises(requests.HTTPError)
    @mock.patch('launchpadstats.stackalytics.requests')
    def test_bad_return_code(self, mock_requests):
        mock_requests.get.return_value = self.bad_response
        launchpadstats.stackalytics.get_stats(dict())
