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

Disambiguation
##############

.. code-block:: python

    from nerd import nerd
    client = nerd.NerdClient()


To disambiguate text (> 5 words):

.. code-block:: python

    client.disambiguate_text(
        "Linux is a name that broadly denotes a family of free and open-source software operating systems (OS) built around the Linux kernel."
    )

To disambiguate a search query

.. code-block:: python

    client.disambiguate_query(
        "python method acronym concrete"
    )


To process a PDF:

.. code-block:: python

    client.disambiguate_pdf(pdfFile, language)


you can supply the language (iso form of two digits, en, fr, etc..) and the entities (only for text) you already know,
using the format:

.. code-block:: python

   {
       'offsetEnd': 5,
       'offsetStart': 0,
       'rawName': 'Linux',
       'wikidataId': 'Q388',
       'wikipediaExternalRef': 6097297
   }


The response is a tuple where the first element is the response body as a dictionary and the second element the error code.
Here an example: 

.. code-block:: python

    (
        {'entities': [
            {
                'domains': ['Computer_Science'],
                'nerd_score': 0.3753,
                'nerd_selection_score': 0.7268,
                'offsetEnd': 5,
                'offsetStart': 0,
                'rawName': 'Linux',
                'type': 'PERSON',
                'wikidataId': 'Q388',
                'wikipediaExternalRef': 6097297
            },
            {
                'domains': ['Computer_Science'],
                'nerd_score': 0.7442,
                'nerd_selection_score': 0.85,
                'offsetEnd': 78,
                'offsetStart': 49,
                'rawName': 'free and open-source software',
                'wikidataId': 'Q506883',
                'wikipediaExternalRef': 1721496
            },
            {
                'domains': ['Electrotechnology', 'Electronics',
                'Computer_Science'],
                'nerd_score': 0.7442,
                'nerd_selection_score': 0.4487,
                'offsetEnd': 96,
                'offsetStart': 79,
                'rawName': 'operating systems',
                'wikidataId': 'Q9135',
                'wikipediaExternalRef': 22194
            },
            {
                'domains': [
                    'Electrotechnology', 'Electronics', 'Computer_Science'
                ],
                'nerd_score': 0.7442,
                'nerd_selection_score': 0.4487,
                'offsetEnd': 100,
                'offsetStart': 98,
                'rawName': 'operating systems',
                'wikidataId': 'Q9135',
                'wikipediaExternalRef': 22194
            },
            {
                'domains': ['Electronics', 'Computer_Science'],
                'nerd_score': 0.743,
                'nerd_selection_score': 0.8383,
                'offsetEnd': 131,
                'offsetStart': 119,
                'rawName': 'Linux kernel',
                'wikidataId': 'Q14579',
                'wikipediaExternalRef': 21347315
            }
        ],
        'global_categories': [
            {'category': 'Finnish inventions',
            'page_id': 27421536,
            'source': 'wikipedia-en',
            'weight': 0.09684039970133569},
           {'category': 'Free software programmed in C',
            'page_id': 11241711,
            'source': 'wikipedia-en',
            'weight': 0.06433942787438053},
           {'category': 'Unix variants',
            'page_id': 10429397,
            'source': 'wikipedia-en',
            'weight': 0.09684039970133569},
           {'category': 'Operating systems',
            'page_id': 693664,
            'source': 'wikipedia-en',
            'weight': 0.12888888710813473},
           {'category': 'Free software',
            'page_id': 693287,
            'source': 'wikipedia-en',
            'weight': 0.06444444355406737},
           {'category': 'Free system software',
            'page_id': 6721544,
            'source': 'wikipedia-en',
            'weight': 0.06433942787438053},
           {'category': 'Software licenses',
            'page_id': 703100,
            'source': 'wikipedia-en',
            'weight': 0.06444444355406737},
           {'category': 'Linux kernel',
            'page_id': 13215678,
            'source': 'wikipedia-en',
            'weight': 0.06433942787438053},
           {'category': 'Monolithic kernels',
            'page_id': 10730969,
            'source': 'wikipedia-en',
            'weight': 0.06433942787438053},
           {'category': '1991 software',
            'page_id': 11167446,
            'source': 'wikipedia-en',
            'weight': 0.09684039970133569},
           {'category': 'Linus Torvalds',
            'page_id': 53479567,
            'source': 'wikipedia-en',
            'weight': 0.09684039970133569}
        ],
        'language': {'conf': 0.9999973266294648, 'lang': 'en'},
        'nbest': False,
        'onlyNER': False,
        'runtime': 107,
        'sentences': [{'offsetEnd': 132, 'offsetStart': 0}],
        'text': 'Linux is a name that broadly denotes a family of free and open-source software operating systems (OS) built around the Linux kernel.'
        },
        200
   )

Batch processing
######################

Here an example:
``processBatch`` requires the input directory, a callback and the number of threads/processes, here an example.
To run it, you have to:
 - create a new branch for instance `/path/of/my/branch`
 - under this new branch, prepare two folders `/input` that containing the input Pdf files and `/output` that will accept the processing result
 - copy the code below in a `runFile.py and put it in `/path/of/my/branch`
 - create a new virtualenv and activate it in this `/path/of/my/branch`
 - install all the requirements needed in the `/path/of/my/branch` directory based on the requirements located in the source directory `$ pip install -r /path/of/entity-fishing-client-python/source/requirements.txt`
 - install entity-fishing **multithread branch** in edit mode (`pip install -e /path/of/entity-fishing-client-python/source`)
 - run it (for instance with the number of threads 5) with `python runFile.py /input /output 5`



.. code-block:: python

   import json
   import os
   import sys
   import time

   from os.path import join

   from nerd_client_batch import NerdBatch

   if len(sys.argv) != 4:
       sys.exit("Missing parameter. Usage: python nerd_batch.py /input/directory /output/directory nbThreads")

   inputPath = sys.argv[1]
   outputPath = sys.argv[2]
   nbThreads = sys.argv[3]


   def saveFile(filename, result):
       output = join(outputPath, os.path.basename(filename)) + ".json"
       with open(output, 'w') as outfile:
           json.dump(result, outfile)

       print("Writing output to " + output)
       return


   start = time.time()
   NerdBatch().processBatch(inputPath, saveFile, int(nbThreads))

   print("Batch processed in " + str(time.time() - start))



KB access
#########
.. code-block:: python

   nerd.get_concept("Q456")


with response

.. code-block:: python

   (
      {
        'rawName': 'Lyon',
        'preferredTerm': 'Lyon',
        'nerd_score': 0,
        'nerd_selection_score': 0,
        'wikipediaExternalRef': 8638634,
        'wikidataId': 'Q456',
        'definitions': [
          {
            'definition': "'''Lyon''' ( or ;, locally: ; ), also known as ''Lyons'', is a city in east-central [[France]], in the [[Auvergne-Rhône-Alpes]] [[Regions of France|region]], about from [[Paris]], from [[Marseille]] and from [[Saint-Étienne]]. Inhabitants of the city are called ''Lyonnais''.",
            'source': 'wikipedia-en',
            'lang': 'en'
          }
        ],
        'domains': [
          'Geology',
          'Sociology'
        ],
        'categories': [
          {
            'source': 'wikipedia-en',
            'category': 'World Heritage Sites in France',
            'page_id': 1178961
          },
          [...]
        ],
        'multilingual': [
          {
            'lang': 'de',
            'term': 'Lyon',
            'page_id': 13964
          },
          {
            'lang': 'es',
            'term': 'Lyon',
            'page_id': 46490
          },
          {
            'lang': 'fr',
            'term': 'Lyon',
            'page_id': 802627
          },
          {
            'lang': 'it',
            'term': 'Lione',
            'page_id': 41786
          }
        ],
        'statements': [
          {
            'conceptId': 'Q456',
            'propertyId': 'P1082',
            'propertyName': 'population',
            'valueType': 'quantity',
            'value': {
              'amount': '+500716',
              'unit': '1',
              'upperBound': '+500717',
              'lowerBound': '+500715'
            }
          },
          {
            'conceptId': 'Q456',
            'propertyId': 'P1082',
            'propertyName': 'population',
            'valueType': 'quantity',
            'value': {
              'amount': '+500716',
              'unit': '1',
              'upperBound': '+500717',
              'lowerBound': '+500715'
            }
          },
          {
            'conceptId': 'Q456',
            'propertyId': 'P1464',
            'propertyName': 'category for people born here',
            'valueType': 'wikibase-item',
            'value': 'Q8061504'
          },
          {
            'conceptId': 'Q456',
            'propertyId': 'P190',
            'propertyName': 'sister city',
            'valueType': 'wikibase-item',
            'value': 'Q5687',
            'valueName': 'Jericho'
          },
          {
            'conceptId': 'Q456',
            'propertyId': 'P190',
            'propertyName': 'sister city',
            'valueType': 'wikibase-item',
            'value': 'Q2079',
            'valueName': 'Leipzig'
          },
          {
            'conceptId': 'Q456',
            'propertyId': 'P190',
            'propertyName': 'sister city',
            'valueType': 'wikibase-item',
            'value': 'Q580',
            'valueName': 'Łódź'
          },
          [...]
        ]
      }
      200
   )


Utilities
#########

Language detection
==================
.. code-block:: python

   nerd.get_language("This is a sentence. This is a second sentence.")


with response

.. code-block:: python

   (
      {
         'sentences':
         [
            {'offsetStart': 0, 'offsetEnd': 19},
            {'offsetStart': 19, 'offsetEnd': 46}
         ]
      },
      200
   )

Segmentation
============
.. code-block:: python

   nerd.segment("This is a sentence. This is a second sentence.")


with response
.. code-block:: python

    (
        {
            "lang": "en",
            "conf": 0.9
        },
        200
    )


Todo
----

The following methods are missing from this client:
* ``termDisambiguation``
