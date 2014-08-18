from setuptools import setup
try:
    # pypi doesn't support the .md format
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''

setup(
    name='stackalyticscli',
    version='0.0.1',
    author='Martina Kollarova',
    author_email='mkollaro@gmail.com',
    url='https://github.com/mkollaro/stackalyticscli',
    packages=['stackalyticscli'],
    license='Apache License, Version 2.0',
    scripts=['bin/stackalyticscli'],
    description='Get data from Stackalytics trough the CLI.',
    long_description=long_description,
    install_requires=['requests'],
    tests_require=['nose'],
)
