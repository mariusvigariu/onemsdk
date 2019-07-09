"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
    name='ONEmSDK',
    version=version,
    description='Python ONEm SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/romeo1m/onemsdk',
    author='romeo1m',
    author_email='romeo.tudureanu@onem.com',
    # Classifiers omitted
    keywords='sdk onem python',
    packages=find_packages(exclude=['contrib', 'docs', 'test']),
    python_requires='>=3.7, <4',
    install_requires=required_packages,
    # entry_points={
    #     'console_scripts': [
    #         'main=main:main',
    #     ],
    # },
    project_urls={
        'Source': 'https://github.com/romeo1m/onemsdk',
    },
)
