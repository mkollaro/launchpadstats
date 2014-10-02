#! /usr/bin/env python
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

import sys
import setuptools
import setuptools.command.test

import launchpadstats

try:
    # pypi doesn't support the .md format
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''


class Tox(setuptools.command.test.test):
    def finalize_options(self):
        super(Tox, self).finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import must be here, because outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


setuptools.setup(
    name='launchpadstats',
    version=launchpadstats.__version__,
    author='Martina Kollarova',
    author_email='mkollaro@gmail.com',
    url='https://github.com/mkollaro/launchpadstats',
    packages=['launchpadstats'],
    license='Apache License, Version 2.0',
    scripts=['bin/launchpadstats', 'bin/launchpadstats-all'],
    description='Get data from Stackalytics trough the CLI.',
    long_description=long_description,
    install_requires=['requests'],
    tests_require=['nose', 'tox>=1.6'],
)
