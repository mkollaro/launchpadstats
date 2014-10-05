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
import sys
import requests
import json

CONTRIBUTION_STATS = {
    "contribution": {
        "loc": 4772,
        "filed_bug_count": 55,
        "patch_set_count": 365,
        "completed_blueprint_count": 1,
        "email_count": 0,
        "marks": {"0": 0, "1": 115, "2": 439, "A": 66, "-2": 2,
                  "WIP": 0, "-1": 73},
        "commit_count": 112,
        "drafted_blueprint_count": 2,
        "change_request_count": 141,
        "resolved_bug_count": 9
        }
    }


def response(status_code=200, content='', headers=None, reason=None):
    res = requests.Response()
    res.status_code = status_code
    if isinstance(content, dict):
        if sys.version_info[0] == 3:
            content = bytes(json.dumps(content), 'utf-8')
        else:
            content = json.dumps(content)
    res._content = content
    res._content_consumed = content
    res.headers = requests.structures.CaseInsensitiveDict(headers or {})
    res.reason = reason
    return res

GOOD_RESPONSE = response(content=CONTRIBUTION_STATS)
BAD_RESPONSE = response(status_code=404, reason="Not Found")
