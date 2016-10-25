import bots.transform as transform


def main(inn, out):
    out.put({'BOTSID': 'Group', 'SenderId': inn.ta_info['frompartner']})
    out.put({'BOTSID': 'Group', 'ReceiverId': inn.ta_info['topartner']})
    out.put({'BOTSID': 'Group',
             'Code': inn.get({'BOTSID': 'ST'}, {'BOTSID': 'AK1', 'AK101': None})})
    out.put({'BOTSID': 'Group',
             'Status': inn.get({'BOTSID': 'ST'}, {'BOTSID': 'AK9', 'AK901': None})})
    out.put({'BOTSID': 'Group',
             'AdvStatus': inn.get({'BOTSID': 'ST'}, {'BOTSID': 'AK9', 'AK905': None})})

    for ak2 in inn.getloop({'BOTSID': 'ST'}, {'BOTSID': 'AK2'}):
        trans = out.putloop({'BOTSID': 'Group'}, {'BOTSID': 'Transaction'})
        trans.put({'BOTSID': 'Transaction',
                   'Code': ak2.get({'BOTSID': 'AK2', 'AK201': None})})
        trans.put({'BOTSID': 'Transaction',
                   'Number': ak2.get({'BOTSID': 'AK2', 'AK202': None})})
        trans.put({'BOTSID': 'Transaction',
                   'Status': ak2.get({'BOTSID': 'AK2'},
                                     {'BOTSID': 'AK5', 'AK501': None})})
        trans.put({'BOTSID': 'Transaction',
                   'AdvStatus': ak2.get({'BOTSID': 'AK2'},
                                        {'BOTSID': 'AK5', 'AK502': None})})
