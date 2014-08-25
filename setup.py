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

from setuptools import setup
try:
    # pypi doesn't support the .md format
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''

setup(
    name='launchpadstats',
    version='0.1.1',
    author='Martina Kollarova',
    author_email='mkollaro@gmail.com',
    url='https://github.com/mkollaro/launchpadstats',
    packages=['launchpadstats'],
    license='Apache License, Version 2.0',
    scripts=['bin/launchpadstats', 'bin/launchpadstats-all'],
    data_files=[
        ('config', ['config.ini']),
    ],
    description='Get data from Stackalytics trough the CLI.',
    long_description=long_description,
    install_requires=['requests'],
    tests_require=['nose'],
)
