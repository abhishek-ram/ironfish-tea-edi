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
        """Update URL of tge webservice to public IP and then POST it"""
        message = etree_to_string(envelope)
        return self.post(
            address.replace('CEV-MSSQL', '66.76.19.198'), message, headers)

    def load(self, url):
        """Update URL of tge webservice to public IP and then GET it"""
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

    def __init__(self):
        if settings.GP_WS_ENABLED:
            cache = SqliteCache()
            session = Session()
            session.auth = HttpNtlmAuth(
                settings.GP_WS_USERNAME, settings.GP_WS_PASSWORD)
            self.client = Client(
                settings.GP_WS_URL,
                transport=GPTransport(session=session, cache=cache)
            )
            self.ws_factory1 = self.client.type_factory('ns1')
            self.ws_factory2 = self.client.type_factory('ns2')
            self.service_context = self.ws_factory2.Context(
                OrganizationKey=self.ws_factory2.CompanyKey(),
                CurrencyType='Local'
            )

    def get_item_by_id(self, item_id):
        if settings.GP_WS_ENABLED:
            return self.client.service.GetItemByKey(
                key=self.ws_factory1.ItemKey(Id=item_id),
                context=self.service_context
            )
        else:
            return {'Description': 'Product Description Here'}
