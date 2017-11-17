# coding: utf-8
import requests


class NerdClient:
    # nerdLocation = "http://128.93.83.104:8090"
    nerdLocation = "http://nerd.huma-num.fr/nerd/service"
    disambiguateService = nerdLocation + "/disambiguate"
    conceptService = nerdLocation + "/kb/concept"
    segmentationService = nerdLocation + "/segmentation"
    maxTextLength = 500  # Approximation.

    def process_text(self, text):
        # text = text.replace("\n", "").replace("\r", "")

        sentence_coordinates = [
            {
                "offsetStart": 0,
                "offsetEnd": len(text)
            }
        ]

        body = {
            "text": text,
            "entities": [],
            "resultLanguages": ["fr", "de", "en"],
            "onlyNER": "false",
            "customisation": "generic"
        }

        total_nb_sentences = len(sentence_coordinates) # Split text in sentences
        sentences_groups = []

        if len(text) > self.maxTextLength:
            status_code, response = self.segmentate(text)

            if status_code == 200:
                sentence_coordinates = response['sentences']
                total_nb_sentences = len(sentence_coordinates)
            else:
                exit(-1)

            print(
                "text too long, splitted in " + str(
                    total_nb_sentences
                ) + " sentences. "
            )
            sentence_groups = self.group_sentences(total_nb_sentences, 3)
        else:
            body['sentence'] = "true"

        if total_nb_sentences > 1:
            body['sentences'] = sentence_coordinates

        if len(sentences_groups) > 0:
            for group in sentences_groups:
                body['processSentence'] = group
                nerd_response, status_code = request(body)

                if 'entities' in nerd_response:
                    body['entities'].extend(nerd_response['entities'])
        else:
            nerd_response, status_code = self.request(body)

        return nerd_response, status_code

    def request(self, body):
        files = {"query": str(body)}

        r = requests.post(self.disambiguateService, files=files,
                          headers={'Accept': 'application/json'})

        status_code = r.status_code
        nerd_response = r.reason
        if status_code == 200:
            nerd_response = r.json()
            if 'entities' in nerd_response:
                body['entities'].extend(nerd_response['entities'])

                # if 'domains' in nerdResponse:
                #     body['domains'].append(nerdResponse['entities'])

        return nerd_response, status_code

    def fetch_concept(self, concept_id, lang="en"):
        url = self.conceptService + "/" + concept_id + "?lang=" + lang
        r = requests.get(url, headers={'Accept': 'application/json'})

        status_code = r.status_code
        nerd_response = r.reason
        if status_code == 200:
            nerd_response = r.json()

        return nerd_response, status_code

    def term_disambiguation(self, terms):
        if isinstance(terms, str):
            terms = [terms, 'history']

        body = {
            "termVector": [],
            "nbest": 0
        }

        for term in terms:
            body["termVector"].append({"term": term})

        r = requests.post(
            self.disambiguateService,
            json=body,
            headers={'Content-Type': 'application/json; charset=UTF-8'}
        )
        status_code = r.status_code
        nerd_response = r.reason

        if status_code == 200:
            nerd_response = r.json()

        return nerd_response, status_code

    def get_nerd_location(self):
        return self.disambiguateService

    def segmentate(self, text):
        """ Call the segmenter in order to split text in sentences. """

        files = {'text': text}
        r = requests.post(self.segmentationService, files=files)
        status_code = r.status_code
        nerd_response = r.reason

        if status_code == 200:
            nerd_response = r.json()

        return status_code, nerd_response

    @staticmethod
    def group_sentences(total_nb_sentences, group_length):

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
