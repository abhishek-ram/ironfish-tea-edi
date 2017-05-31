import requests
import bots.transform as transform
from bots import botslib
import json


def connect(channeldict):
    pass


def main(channeldict, *args, **kargs):
    output_dir = botslib.join(channeldict['path'])
    botslib.dirshouldbethere(output_dir)
    url = 'http://{}:{}/api/shipping_invoice/'.format(
        channeldict['host'], channeldict['port'])
    custom_headers = {
        'Authorization': 'Token {}'.format(channeldict['parameters']),
        'Content-Type': 'application/json'
    }
    invoices = requests.get(url, headers=custom_headers)

    for invoice in invoices.json():
        filename = botslib.join(output_dir, str(
            transform.unique('Shipping Invoice Get')) + '.json')
        output_file = open(filename, 'wb')
        output_file.write(json.dumps({'Invoice': invoice}))
        output_file.close()

        # Mark invoice as processed
        url = 'http://{}:{}/api/shipping_invoice/{}/processed/'.format(
            channeldict['host'], channeldict['port'], invoice['invoice_id'])
        process_invoice = requests.post(url, headers=custom_headers)
        process_invoice.raise_for_status()

        # Return the filename
        yield filename


def disconnect(channeldict):
    pass
