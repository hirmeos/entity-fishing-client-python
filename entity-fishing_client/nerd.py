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

    api_base = "http://nerd.huma-num.fr/nerd/service"
    disambiguate_service = urljoin(api_base, "disambiguate")
    concept_service = urljoin(api_base, "kb/concept")
    segmentation_service = urljoin(api_base, "segmentation")
    max_text_length = 500  # Approximation.
    supported_languages = ["fr", "de", "en"]

    def __init__(self):
        super(NerdClient, self).__init__(base_url=self.api_base)

    def _process_text(self, text):
        """ Prepare text for disambiguation.

        Args:
            text (str): Text to be processed.

        Returns:
            str: Body ready to be submitted to the API.
        """

        sentence_coordinates = [
            {
                "offsetStart": 0,
                "offsetEnd": len(text)
            }
        ]

        body = {
            "text": text,
            "entities": [],
            "resultLanguages": self.supported_languages,
            "onlyNER": "false",
            "customisation": "generic"
        }

        total_nb_sentences = len(sentence_coordinates)  # Sentences from text.
        sentences_groups = []

        if len(text) > self.max_text_length:
            res, status_code = self.segmentate(text)

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

                res, status_code = self.disambiguate(body, prepared=True)

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

    def disambiguate(self, text, prepared=False):
        """ Call the disambiguation service in order to get meanings.

        Args:
            text (str): Text to be disambiguated.
            prepared (bool): Whether text must be prepared for API before.

        Returns:
            dict, int: API response and API status.
        """

        body = self._process_text(text) if not prepared else text
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
