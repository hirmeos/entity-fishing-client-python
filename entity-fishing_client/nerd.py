import json
import sys

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from zenlog import logging

from .client import ApiClient

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
    api_base = "http://nerd.huma-num.fr/test/service/"
    max_text_length = 500  # Approximation.

    def __init__(self, apiBase=api_base):
        super(NerdClient, self).__init__(base_url=apiBase)
        if not apiBase.endswith('/'):
            apiBase = apiBase + '/'
        api_base = apiBase

        self.disambiguate_service = urljoin(api_base, "disambiguate")
        self.concept_service = urljoin(api_base, "kb/concept")
        self.segmentation_service = urljoin(api_base, "segmentation")

    def _process_text(self, body):
        """ Prepare text for disambiguation.

        Args:
            text (str): Text to be processed.
            language (str): if language known
            entities (list): list of entities of already disambiguated entities

        Returns:
            str: Body ready to be submitted to the API.
        """

        text = body['text']

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
                'Text too long, split in {} sentences; building groups.'.format(
                    total_nb_sentences
                )
            )
            sentences_groups = self._group_sentences(total_nb_sentences, 3)
        else:
            body['sentence'] = "true"

        if total_nb_sentences > 1:
            body['sentences'] = sentence_coordinates

        if len(sentences_groups) > 0:
            final_body = body

            for group in sentences_groups:
                final_body['processSentence'] = group
                body = json.dumps(final_body)

                res, status_code = self.disambiguateText(body, prepared=True)

                if status_code == 200 and 'entities' in res:
                    final_body['entities'] = res[u'entities']

        logger.debug('About to submit the following query {}'.format(body))

        return body

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

    def disambiguatePdf(self, file, language=None, entities=None):
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

        files = {'query': str(body), 'file': (file, open(file, 'rb'), 'application/pdf', {'Expires': '0'})}

        res, status = self.post(
            self.disambiguate_service,
            files=files,
            headers={'Accept': 'application/json'},
        )

        if status == 200:
            return self.decode(res), status

        logger.debug('Disambiguation failed with error ' + str(status))

    def disambiguateText(self, text, language=None, entities=None, prepared=False):
        """ Call the disambiguation service in order to get meanings.

        Args:
            text (str): Text to be disambiguated.
            language (str): language of text (if known)
            prepared (bool): Whether text must be prepared for API before.

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

        body = self._process_text(body) if not prepared else text

        files = {'query': str(body)}

        res, status = self.post(
            self.disambiguate_service,
            files=files,
            headers={'Accept': 'application/json'},
        )

        if status == 200:
            return self.decode(res), status

        logger.debug('Disambiguation failed.')

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

        if status_code == 200:
            return self.decode(res), status_code

        logger.debug('Segmentation failed.')

    def get_language(self, text):
        """ Recognise the language of the text in input

        Args:
              id (str): The text whose the language needs to be recognised

        Returns:
            dict, int: A dict containing the recognised language and the confidence score
        """
        files = {'text': text}
        res, status_code = self.post(self.segmentation_service, files=files)

        if status_code == 200:
            return self.decode(res), status_code

        logger.debug('Language recognition failed.')

    def get_concept(self, conceptId):
        """ Fetch the concept from the Knowledge base

        Args:
              id (str): The concept id to be fetched, it can be Wikipedia page id or Wikiedata id

        Returns:
            dict, int: A dict containing the concept information; an integer reprsenting the response code
        """
        url = urljoin(self.concept_service + '/', conceptId)

        res, status_code = self.get(url)

        if status_code == 200:
            return self.decode(res), status_code

        logger.debug('Fetch concept failed.')
