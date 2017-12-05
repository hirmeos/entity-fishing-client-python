""" Generic API Client """
from copy import deepcopy
import json
import logging
import requests
from urlparse import urljoin


logger = logging.getLogger(__name__)


class ApiClient(object):
    """ Client to interact with a generic Rest API.

    Subclasses should implement functionality accordingly with the provided
    service methods, i.e. ``get``, ``post``, ``put`` and ``delete``.
    """

    ResultParser = BaseResponse
    ErrorParser = ErrorResponse
    acceptType = 'application/json'

    def __init__(
            self,
            base_url,
            username,
            api_key,
            status_endpoint=None,
            timeout=60
    ):
        """ Initialise client.

        Args:
            base_url (str): The base URL to the service being used.
            username (str): The username to authenticate with.
            api_key (str): The API key to authenticate with.
            timeout (int): Maximum time before timing out.
        """
        self.base_url = base_url
        self.username = username
        self.api_key = api_key
        self.status_endpoint = urljoin(self.base_url, self.status_endpoint)
        self.timeout = timeout

    @staticmethod
    def encode(request, data):
        """ Add request content data to request body, set Content-type header.

        Should be overridden by subclasses if not using JSON encoding.

        Args:
            request (HTTPRequest): The request object.
            data (dict, None): Data to be encoded.

        Returns:
            HTTPRequest: The request object.
        """
        if data is None:
            return request

        request.add_header('Content-Type', 'application/json')
        request.data = json.dumps(data)

        return request

    @staticmethod
    def decode(response):
        """ Decode the returned data in the response.

        Should be overridden by subclasses if something else than JSON is
        expected.

        Args:
            response (HTTPResponse): The response object.

        Returns:
            dict or None.
        """
        try:
            return response.json()
        except ValueError as e:
            return e.message

    def get_credentials(self):
        """ Returns parameters to be added to authenticate the request.

        This lives on its own to make it easier to re-implement it if needed.

        Returns:
            dict: A dictionary containing the credentials.
        """
        return {"username": self.username, "api_key": self.api_key}

    def call_api(
            self,
            method,
            url,
            headers=None,
            params=None,
            data=None,
            timeout=None
    ):
        """ Call API.

        This returns object containing data, with error details if applicable.

        Args:
            method (str): The HTTP method to use.
            url (str): Resource location relative to the base URL.
            headers (dict or None): Extra request headers to set.
            params (dict or None): Query-string parameters.
            data (dict or None): Request body contents for POST or PUT requests.
            timeout (int): Maximum time before timing out.

        Returns:
            ResultParser or ErrorParser.
        """
        method = method.upper()
        headers = deepcopy(headers) or {}
        headers['Accept'] = self.acceptType
        params = deepcopy(params) or {}
        data = data or {}
        timeout = timeout or self.timeout

        params.update(self.get_credentials())

        url = "{b}{u}".format(b=self.base_url, u=url)

        logger.debug(
            "ApiClient performing call: method=`{m}` "
            "url=`{u}` headers=`{h}` timeout=`{t}`".format(
                m=method,
                u=url,
                h=headers,
                t=timeout,
            )
        )

        r = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data,
        )

        return self.ResultParser(self.decode(r))

    def get(self, url, params=None, **kwargs):
        """ Call the API with a GET request.

        Args:
            url (str): Resource location relative to the base URL.
            params (dict or None): Query-string parameters.

        Returns:
            ResultParser or ErrorParser.
        """
        return self.call_api("GET", url, params, **kwargs)

    def delete(self, url, params=None, **kwargs):
        """ Call the API with a DELETE request.

        Args:
            url (str): Resource location relative to the base URL.
            params (dict or None): Query-string parameters.

        Returns:
            ResultParser or ErrorParser.
        """
        return self.call_api("DELETE", url, params, **kwargs)

    def put(self, url, params=None, data=None, **kwargs):
        """ Call the API with a PUT request.

        Args:
            url (str): Resource location relative to the base URL.
            params (dict or None): Query-string parameters.
            data (dict or None): Request body contents.

        Returns:
            An instance of ResultParser or ErrorParser.
        """
        return self.call_api("PUT", url, params=params, data=data, **kwargs)

    def post(self, url, params=None, data=None, **kwargs):
        """ Call the API with a POST request.

        Args:
            url (str): Resource location relative to the base URL.
            params (dict or None): Query-string parameters.
            data (dict or None): Request body contents.

        Returns:
            An instance of ResultParser or ErrorParser.
        """
        return self.call_api("POST", url, params=params, data=data, **kwargs)

    def service_status(self, **kwargs):
        """ Call the API to get the status of the service.

        Returns:
            An instance of ResultParser or ErrorParser.
        """
        return self.call_api(
            'GET',
            self.status_endpoint,
            params={'format': 'json'},
            **kwargs
        )
