import requests


def connect(channeldict):
    pass


def main(channeldict, filename, *args, **kwargs):
    url = 'http://{}:{}/api/process_acknowledgment'.format(
        channeldict['host'], channeldict['port'])
    custom_headers = {
        'Authorization': 'Token {}'.format(channeldict['parameters']),
        'Content-Type': 'application/json'
    }
    with open(filename, 'r') as content_file:
        json_data = content_file.read()
        post_ack = requests.post(url, headers=custom_headers, data=json_data)
    post_ack.raise_for_status()


def disconnect(channeldict):
    pass