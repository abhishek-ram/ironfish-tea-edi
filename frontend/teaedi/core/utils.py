from django.conf import settings
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.wsdl.utils import etree_to_string
from six.moves.urllib.parse import urlparse
import os
from requests_ntlm import HttpNtlmAuth
from requests import Session


class GPTransport(Transport):

    def post_xml(self, address, envelope, headers):
        """Post the envelope xml element to the given address with the headers.

        This method is intended to be overriden if you want to customize the
        serialization of the xml element. By default the body is formatted
        and encoded as utf-8. See ``zeep.wsdl.utils.etree_to_string``.

        """
        message = etree_to_string(envelope)
        return self.post(
            address.replace('CEV-MSSQL', '66.76.19.198'), message, headers)

    def load(self, url):
        """Load the content from the given URL"""
        if not url:
            raise ValueError("No url given to load")
        actual_url = url.replace('CEV-MSSQL', '66.76.19.198')
        scheme = urlparse(actual_url).scheme
        if scheme in ('http', 'https'):

            if self.cache:
                response = self.cache.get(actual_url)
                if response:
                    return bytes(response)

            content = self._load_remote_data(actual_url)

            if self.cache:
                self.cache.add(actual_url, content)

            return content

        elif scheme == 'file':
            if url.startswith('file://'):
                url = url[7:]

        with open(os.path.expanduser(actual_url), 'rb') as fh:
            return fh.read()


class GPWebService(object):
    """Class for interacting with MS Dynamics GP Web Services"""

    def __index__(self):
        if not settings.DEBUG:
            cache = SqliteCache()
            session = Session()
            session.auth = HttpNtlmAuth(
                settings.GP_WS_USERNAME, settings.GP_WS_PASSWORD)
            self.client = Client(
                settings.GP_WS_URL,
                transport=GPTransport(session=session, cache=cache)
            )

    def get_item_by_id(self, item_id):
        print 'jere'
        if settings.DEBUG:
            print 'jere'
            return {'Description': 'Product Description Here'}
        else:
            factory1 = self.client.type_factory('ns1')
            factory2 = self.client.type_factory('ns2')

            context = factory2.Context(
                OrganizationKey=factory2.CompanyKey(1), CurrencyType='Local')
            return self.client.service.GetItemByKey(
                key=factory1.ItemKey(Id=item_id), context=context)
