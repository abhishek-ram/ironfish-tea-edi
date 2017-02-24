from django.conf import settings
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.wsdl.utils import etree_to_string
from six.moves.urllib.parse import urlparse
from requests_ntlm import HttpNtlmAuth
from requests import Session
from decimal import Decimal
import os
import datetime


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
            cache = SqliteCache(timeout=30 * 24 * 60 * 60)
            session = Session()
            session.auth = HttpNtlmAuth(
                settings.GP_WS_USERNAME, settings.GP_WS_PASSWORD)
            self.client = Client(
                settings.GP_WS_URL,
                transport=GPTransport(session=session, cache=cache)
            )
            self.ws_factory1 = self.client.type_factory('ns1')
            self.ws_factory2 = self.client.type_factory('ns2')
            company = self.ws_factory2.CompanyKey(settings.GP_COMPANY_ID)
            self.service_context = self.ws_factory2.Context(
                OrganizationKey=company,
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

    def get_invoice_list(self, customer_id):
        if settings.GP_WS_ENABLED:
            criteria = {
                'TransactionState': self.ws_factory1.ListRestrictionOfNullableOfSalesTransactionState(
                    'Work'),
                'CustomerId': self.ws_factory1.LikeRestrictionOfString(
                    customer_id),
                'Scope': 'Return All'
            }
            return self.client.service.GetSalesInvoiceList(
                criteria=criteria, context=self.service_context)
        else:
            return [{
                'Key': {
                    'CompanyKey': {
                        'Id': 2
                    },
                    'Id': '092306'
                },
            }]

    def get_invoice_detail(self, invoice_id):

        if settings.GP_WS_ENABLED:
            return self.client.service.GetSalesInvoiceByKey(
                key={'Id': invoice_id}, context=self.service_context)

        else:
            return {
                'Key': {
                    'CompanyKey': {
                        'Id': 2L
                    },
                    'Id': '092306'
                },
                'BatchKey': {
                    'CompanyKey': {
                        'Id': 1L
                    },
                    'Source': 'Sales Entry',
                    'Id': 'Transfer 02/24',
                    'CreatedDateTime': datetime.datetime(1900, 1, 1, 0, 0)
                },
                'Type': 'Invoice',
                'Date': datetime.datetime(2017, 2, 8, 0, 0),
                'CustomerName': 'Texas Education Agency',
                'CustomerPONumber': '00001251811',
                'RequestedShipDate': datetime.datetime(2017, 1, 25, 0, 0),
                'Comment': 'We Appreciate Your Business',
                'LineTotalAmount': {
                    'Currency': 'USD',
                    'Value': Decimal('2120.00000'),
                    'DecimalDigits': 2L
                },
                'TotalAmount': {
                    'Currency': 'USD',
                    'Value': Decimal('2120.00000'),
                    'DecimalDigits': 2L
                },
                'ActualShipDate': datetime.datetime(2017, 2, 6, 0, 0),
                'InvoiceDate': datetime.datetime(2017, 2, 8, 0, 0),
                'OriginalSalesDocumentKey': {
                    'CompanyKey': None,
                    'Id': 'TEA0000125614'
                },
                'ShipToAddressKey': {
                    'CompanyKey': {
                        'Id': 2L
                    },
                    'CustomerKey': {
                        'CompanyKey': {
                            'Id': 2L
                        },
                        'Id': '7TEX701'
                    },
                    'Id': '187906'
                },
                'ShipToAddress': {
                    'Extensions': None,
                    'Line1': 'Breanna Murphy bmurphy@leggettisd.net',
                    'Line2': 'Leggett High School',
                    'Line3': 'P.O. Box 68',
                    'City': 'Leggett',
                    'State': 'TX',
                    'PostalCode': '77350',
                    'CountryRegion': 'United States',
                },
                'UserDefined': {
                    'Date01': datetime.datetime(2017, 2, 8, 0, 0),
                    'Date02': None,
                    'List01': '1',
                    'List02': '12.00',
                    'List03': None,
                    'Text01': '6',
                    'Text02': None,
                    'Text03': '0000123394',
                    'Text04': '0000141474',
                    'Text05': '1z79x8540353316852'
                },
                'Lines': {
                    'SalesInvoiceLine': [
                        {
                            'UnitPrice': {
                                'Currency': 'USD',
                                'Value': Decimal('801.00000'),
                                'DecimalDigits': 2
                            },
                            'TotalAmount': {
                                'Currency': 'USD',
                                'Value': Decimal('801.00000'),
                                'DecimalDigits': 2
                            },
                            'Quantity': {
                                'Value': Decimal('1.00000'),
                                'DecimalDigits': 0
                            },
                            'Discount': {
                                'Amount': None,
                                'Percent': {
                                    'Value': Decimal('0'),
                                    'DecimalDigits': 2L
                                }
                            },
                            'ItemDescription': 'Some Product Description',
                            'UofM': 'Each',
                            'ItemKey': {
                                'CompanyKey': {
                                    'Id': 2L
                                },
                                'Id': '9781603339056'
                            },
                        },
                    ]
                },
            }
