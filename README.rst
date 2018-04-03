HIRMEOS Entity Fishing client
=============================

.. image:: http://img.shields.io/:license-apache-blue.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0.html

.. image:: https://travis-ci.org/hirmeos/entity-fishing-client-python.svg?branch=master
   :target: https://travis-ci.org/hirmeos/entity-fishing-client-python


Python client to query the `Entity Fishing service API`_ developed in the context of the EU H2020 HIRMEOS project (WP3).
For more information about entity-fishing, please check the `Entity Fishing Documentation`_. 

.. _Entity Fishing service API: http://github.com/kermitt2/nerd
.. _Entity Fishing Documentation: http://nerd.readthedocs.io


Installation
------------

The client can be installed using `pip`:

   pip install entity-fishing-client

Usage
-----

.. code-block:: python

    from nerd import nerd
    client = nerd.NerdClient()

    client.disambiguate(
        "Linux is a name that broadly denotes a family of free and open-source software operating systems (OS) built around the Linux kernel."
    )

With the following example response:

.. code-block:: python

    (
        {u'entities': [
            {
                u'domains': [u'Computer_Science'],
                u'nerd_score': 0.3753,
                u'nerd_selection_score': 0.7268,
                u'offsetEnd': 5,
                u'offsetStart': 0,
                u'rawName': u'Linux',
                u'type': u'PERSON',
                u'wikidataId': u'Q388',
                u'wikipediaExternalRef': 6097297
            },
            {
                u'domains': [u'Computer_Science'],
                u'nerd_score': 0.7442,
                u'nerd_selection_score': 0.85,
                u'offsetEnd': 78,
                u'offsetStart': 49,
                u'rawName': u'free and open-source software',
                u'wikidataId': u'Q506883',
                u'wikipediaExternalRef': 1721496
            },
            {
                u'domains': [u'Electrotechnology', u'Electronics',
                u'Computer_Science'],
                u'nerd_score': 0.7442,
                u'nerd_selection_score': 0.4487,
                u'offsetEnd': 96,
                u'offsetStart': 79,
                u'rawName': u'operating systems',
                u'wikidataId': u'Q9135',
                u'wikipediaExternalRef': 22194
            },
            {
                u'domains': [
                    u'Electrotechnology', u'Electronics', u'Computer_Science'
                ],
                u'nerd_score': 0.7442,
                u'nerd_selection_score': 0.4487,
                u'offsetEnd': 100,
                u'offsetStart': 98,
                u'rawName': u'operating systems',
                u'wikidataId': u'Q9135',
                u'wikipediaExternalRef': 22194
            },
            {
                u'domains': [u'Electronics', u'Computer_Science'],
                u'nerd_score': 0.743,
                u'nerd_selection_score': 0.8383,
                u'offsetEnd': 131,
                u'offsetStart': 119,
                u'rawName': u'Linux kernel',
                u'wikidataId': u'Q14579',
                u'wikipediaExternalRef': 21347315
            }
        ],
        u'global_categories': [
            {u'category': u'Finnish inventions',
            u'page_id': 27421536,
            u'source': u'wikipedia-en',
            u'weight': 0.09684039970133569},
           {u'category': u'Free software programmed in C',
            u'page_id': 11241711,
            u'source': u'wikipedia-en',
            u'weight': 0.06433942787438053},
           {u'category': u'Unix variants',
            u'page_id': 10429397,
            u'source': u'wikipedia-en',
            u'weight': 0.09684039970133569},
           {u'category': u'Operating systems',
            u'page_id': 693664,
            u'source': u'wikipedia-en',
            u'weight': 0.12888888710813473},
           {u'category': u'Free software',
            u'page_id': 693287,
            u'source': u'wikipedia-en',
            u'weight': 0.06444444355406737},
           {u'category': u'Free system software',
            u'page_id': 6721544,
            u'source': u'wikipedia-en',
            u'weight': 0.06433942787438053},
           {u'category': u'Software licenses',
            u'page_id': 703100,
            u'source': u'wikipedia-en',
            u'weight': 0.06444444355406737},
           {u'category': u'Linux kernel',
            u'page_id': 13215678,
            u'source': u'wikipedia-en',
            u'weight': 0.06433942787438053},
           {u'category': u'Monolithic kernels',
            u'page_id': 10730969,
            u'source': u'wikipedia-en',
            u'weight': 0.06433942787438053},
           {u'category': u'1991 software',
            u'page_id': 11167446,
            u'source': u'wikipedia-en',
            u'weight': 0.09684039970133569},
           {u'category': u'Linus Torvalds',
            u'page_id': 53479567,
            u'source': u'wikipedia-en',
            u'weight': 0.09684039970133569}
        ],
        u'language': {u'conf': 0.9999973266294648, u'lang': u'en'},
        u'nbest': False,
        u'onlyNER': False,
        u'runtime': 107,
        u'sentences': [{u'offsetEnd': 132, u'offsetStart': 0}],
        u'text': u'Linux is a name that broadly denotes a family of free and open-source software operating systems (OS) built around the Linux kernel.'
        },
        200
   )

Todo
----

The following methods are missing from this client:

* ``fetchConcept``
* ``termDisambiguation``
* ``getNerdLocation``
* ``queryDisambiguation``
* ``pdfDisambiguation``
