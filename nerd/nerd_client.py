import sys

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from zenlog import logging

from nerd.client import ApiClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '\n\n %(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
stream.setFormatter(formatter)
logger.addHandler(stream)


class NerdClient(ApiClient):
    api_base = "http://nerd.huma-num.fr/nerd/service/"
    max_text_length = 500  # Approximation.
    sentences_per_group = 10  # Number of sentences per group

    def __init__(self, apiBase=api_base):
        super(NerdClient, self).__init__(base_url=apiBase)
        if not apiBase.endswith('/'):
            apiBase = apiBase + '/'
        api_base = apiBase

        self.disambiguate_service = urljoin(api_base, "disambiguate")
        self.concept_service = urljoin(api_base, "kb/concept")
        self.segmentation_service = urljoin(api_base, "segmentation")
        self.language_service = urljoin(api_base, "language")

    def _process_query(self, query, prepared=False):
        """ Process query recursively, if the text is too long,
        it is split and processed bit a bit.

        Args:
            query (sdict): Text to be processed.
            prepared (bool): True when the query is ready to be submitted via
            POST request.
        Returns:
            str: Body ready to be submitted to the API.
        """

        # Exit condition and POST
        if prepared is True:
            files = {'query': str(query)}

            logger.debug('About to submit the following query {}'.format(query))

            res, status = self.post(
                self.disambiguate_service,
                files=files,
                headers={'Accept': 'application/json'},
            )

            if status == 200:
                return self.decode(res), status
            else:
                logger.debug('Disambiguation failed.')
                return None, status

        text = query['text']

        sentence_coordinates = [
            {
                "offsetStart": 0,
                "offsetEnd": len(text)
            }
        ]

        total_nb_sentences = len(sentence_coordinates)  # Sentences from text.
        sentences_groups = []

        if len(text) > self.max_text_length:
            res, status_code = self.segment(text)

            if status_code == 200:
                sentence_coordinates = res['sentences']
                total_nb_sentences = len(sentence_coordinates)
            else:
                logger.error('Error during the segmentation of the text.')

            logger.debug(
                'Text too long, split in {} sentences; building groups of {} '
                'sentences.'.format(
                    total_nb_sentences, self.sentences_per_group
                )
            )
            sentences_groups = self._group_sentences(
                total_nb_sentences,
                self.sentences_per_group
            )
        else:
            query['sentence'] = "true"

        if total_nb_sentences > 1:
            query['sentences'] = sentence_coordinates

        if len(sentences_groups) > 0:
            for group in sentences_groups:
                query['processSentence'] = group

                res, status_code = self._process_query(query, prepared=True)

                if status_code == 200:
                    if 'entities' in res:
                        query['entities'] = res[u'entities']
                    query['language'] = res[u'language']
                else:
                    logger.error(
                        "Error when processing the query {}".format(query)
                    )
                    return None, status_code

        else:
            res, status_code = self._process_query(query, prepared=True)

            if status_code == 200:
                query['language'] = res[u'language']
                if 'entities' in res:
                    query['entities'] = res[u'entities']
            else:
                logger.error("Error when processing the query {}".format(query))
                return None, status_code

        return query, status_code

    @staticmethod
    def _group_sentences(total_nb_sentences, group_length):
        """ Split sentences in groups, given a specific group length.

        Args:
            total_nb_sentences (int): Total available sentences.
            group_length (int): Limit of length for each group.

        Returns:
            list: Contains groups (lists) of sentences.
        """
        sentences_groups = []
        current_sentence_group = []

        for i in range(0, total_nb_sentences):
            if i % group_length == 0:
                if len(current_sentence_group) > 0:
                    sentences_groups.append(current_sentence_group)
                current_sentence_group = [i]
            else:
                current_sentence_group.append(i)

        if len(current_sentence_group) > 0:
            sentences_groups.append(current_sentence_group)

        return sentences_groups

    def disambiguate_pdf(self, file, language=None, entities=None):
        """ Call the disambiguation service in order to process a pdf file .

        Args:
            pdf (file): PDF file to be disambiguated.
            language (str): language of text (if known)

        Returns:
            dict, int: API response and API status.
        """

        body = {
            "customisation": "generic"
        }

        if language:
            body['language'] = {"lang": language}

        if entities:
            body['entities'] = entities

        files = {
            'query': str(body),
            'file': (
                file,
                open(file, 'rb'),
                'application/pdf',
                {'Expires': '0'}
            )
        }

        res, status = self.post(
            self.disambiguate_service,
            files=files,
            headers={'Accept': 'application/json'},
        )

        if status != 200:
            logger.debug('Disambiguation failed with error ' + str(status))

        return self.decode(res), status

    def disambiguate_terms(self, terms, language="en", entities=None):
        """ Call the disambiguation service in order to get meanings.

            Args:
                terms (obj): list of objects of term, weight
                language (str): language of text, english if not specified
                entities (list): list of entities or mentions to be supplied by
                    the user.

            Returns:
                dict, int: API response and API status.
            """

        body = {
            "termVector": terms,
            "entities": [],
            "onlyNER": "false",
            "customisation": "generic"
        }

        body['language'] = {"lang": language}

        if entities:
            body['entities'] = entities

        files = {'query': str(body)}

        logger.debug('About to submit the following query {}'.format(body))

        res, status = self.post(
            self.disambiguate_service,
            files=files,
            headers={'Accept': 'application/json'},
        )

        if status == 200:
            return self.decode(res), status
        else:
            logger.debug('Disambiguation failed.')
            return None, status

    def disambiguate_text(self, text, language=None, entities=None):
        """ Call the disambiguation service in order to get meanings.

        Args:
            text (str): Text to be disambiguated.
            language (str): language of text (if known)
            entities (list): list of entities or mentions to be supplied by
                the user.

        Returns:
            dict, int: API response and API status.
        """

        body = {
            "text": text,
            "entities": [],
            "onlyNER": "false",
            "customisation": "generic"
        }

        if language:
            body['language'] = {"lang": language}

        if entities:
            body['entities'] = entities

        result, status_code = self._process_query(body)

        if status_code != 200:
            logger.debug('Disambiguation failed.')

        return result, status_code

    def disambiguate_query(self, query, language=None, entities=None):
        """ Call the disambiguation service in order to disambiguate a search query.

        Args:
            text (str): Query to be disambiguated.
            language (str): language of text (if known)
            entities (list): list of entities or mentions to be supplied by
                the user.

        Returns:
            dict, int: API response and API status.
        """

        body = {
            "shortText": query,
            "entities": [],
            "onlyNER": "false",
            "customisation": "generic"
        }

        if language:
            body['language'] = {"lang": language}

        if entities:
            body['entities'] = entities

        files = {'query': str(body)}

        logger.debug('About to submit the following query {}'.format(body))

        res, status = self.post(
            self.disambiguate_service,
            files=files,
            headers={'Accept': 'application/json'},
        )

        if status == 200:
            return self.decode(res), status
        else:
            logger.debug('Disambiguation failed.')
            return None, status

    def segment(self, text):
        """ Call the segmenter in order to split text in sentences.

        Args:
            text (str): Text to be segmented.

        Returns:
            dict, int: A dict containing a list of dicts with the offsets of
                each sentence; an integer representing the response code.
        """

        files = {'text': text}
        res, status_code = self.post(self.segmentation_service, files=files)

        if status_code != 200:
            logger.debug('Segmentation failed.')

        return self.decode(res), status_code

    def get_language(self, text):
        """ Recognise the language of the text in input

        Args:
              id (str): The text whose the language needs to be recognised

        Returns:
            dict, int: A dict containing the recognised language and the
                confidence score.
        """
        files = {'text': text}
        res, status_code = self.post(self.language_service, files=files)

        if status_code != 200:
            logger.debug('Language recognition failed.')

        return self.decode(res), status_code

    def get_concept(self, conceptId, lang='en'):
        """ Fetch the concept from the Knowledge base

        Args:
              id (str): The concept id to be fetched, it can be Wikipedia
                page id or Wikiedata id.

        Returns:
            dict, int: A dict containing the concept information; an integer
                representing the response code.
        """
        url = urljoin(self.concept_service + '/', conceptId)

        res, status_code = self.get(url, params={'lang': lang})

        if status_code != 200:
            logger.debug('Fetch concept failed.')

        return self.decode(res), status_code
