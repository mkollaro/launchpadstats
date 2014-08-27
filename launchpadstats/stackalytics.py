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


LOG = logging.getLogger('launchpadstats')


STACKALYTICS_URL = 'http://stackalytics.com/'


def get_stats(params):
    """Query Stackalytics 'contribution' module with `params`.

    :param params: a dictionary of data passed to the 'contribution' module,
        e.g. 'user_id', 'release', 'company'.  The values can contain more
        items seprated by commas, e.g.  `{'user_id': 'user1,user2,user3'}`.
    """
    MODULE = 'api/1.0/contribution'
    params = dict(params)
    LOG.info("Using parameters: %s", params)
    r = requests.get(STACKALYTICS_URL + MODULE, params=params)
    LOG.info(r.url)
    r.raise_for_status()
    return r.json()


def check_users_exist(user_ids):
    """Check if the users exist in Stackalytics (and therefore in Launchpad).

    TODO: use grequests for async requests to make this faster

    :param user_ids: list of user_id items
    :returns: dictionary with user_ids as keys and booleans as values. The user
        is registered in Launchpad/Stackalytics iff `result[user] == True`.
    """
    result = dict()
    for user in user_ids:
        r = requests.get(STACKALYTICS_URL, params={'user_id': user})
        LOG.info("Checking %s", r.url)
        if r.status_code == requests.codes.ok:
            result[user] = True
        else:
            result[user] = False
            LOG.warning("User_id '%s' is not registered in Launchpad", user)
    return result
