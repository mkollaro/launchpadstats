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

import requests
import logging


LOG = logging.getLogger('stackalyticscli')


STACKALYTICS_URL = 'http://stackalytics.com/'
COMPANY = 'Red Hat'
PROJECT_TYPE = 'OpenStack'


def get_stats(params):
    """Query Stackalytics 'contribution' module with `params`.

    :param params: a dictionary of data passed to the 'contribution' module,
        e.g. 'user_id', 'release', 'company'. If 'company' is not specified,
        use `COMPANY`, if 'project_type' is not specified, use 'OpenStack'.
        The values can contain more items seprated by commas, e.g.
        `{'user_id': 'user1,user2,user3'}`.
    """
    MODULE = 'api/1.0/contribution'
    params = dict(params)
    if 'company' not in params:
        params['company'] = COMPANY
    if 'project_type' not in params:
        params['project_type'] = PROJECT_TYPE

    LOG.info("Using parameters: %s", params)
    r = requests.get(STACKALYTICS_URL + MODULE, params=params)
    LOG.info(r.url)
    r.raise_for_status()
    return r.json()
