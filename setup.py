from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

import unittest


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('nerd/tests', pattern='test_*.py')
    return test_suite


setup(
    name='entity-fishing-client',
    version='0.7.0',
    description='A minimal client for entity-fishing service.',
    long_description=long_description,
    url='https://github.com/Hirmeos/entity-fishing-client-python',
    author='Francesco de Virgilio, Luca Foppiano',
    author_email='francesco.devirgilio@ubiquitypress.com, luca.foppiano@inria.fr',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        # 'Topic :: Text processing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['named entity recognition', 'entity matching', 'entity recognition'],
    install_requires=['requests', 'zenlog'],
    packages=['nerd'],
    # package_dir={'nerd': 'entity-fishing_client'},
    zip_safe=False,
    test_suite='setup.my_test_suite'
)
