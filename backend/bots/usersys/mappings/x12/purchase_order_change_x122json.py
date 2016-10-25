import bots.transform as transform


def main(inn, out):
    out.put({'BOTSID': 'Header', 'SenderId': inn.ta_info['frompartner']})
    out.put({'BOTSID': 'Header', 'ReceiverId': inn.ta_info['topartner']})
    out.put({'BOTSID': 'Header',
             'OrderType': inn.get({'BOTSID': 'ST'},
                                  {'BOTSID': 'BCH', 'BCH02': None})})

    doc_num = inn.get({'BOTSID': 'ST'}, {'BOTSID': 'BCH', 'BCH03': None})
    inn.ta_info['botskey'] = out.ta_info['botskey'] = doc_num
    out.put({'BOTSID': 'Header', 'OrderNumber': doc_num})

    order_date = inn.get({'BOTSID': 'ST'}, {'BOTSID': 'BCH', 'BCH06.02': None}) + \
                 inn.get({'BOTSID': 'ST'}, {'BOTSID': 'BCH', 'BCH06.01': None})
    out.put({'BOTSID': 'Header', 'OrderDate': order_date})

    out.put({'BOTSID': 'Header',
             'ChangeOrderSeq': inn.get({'BOTSID': 'ST'},
                                       {'BOTSID': 'BCH', 'BCH05': None})})

    out.put({'BOTSID': 'Header',
             'ContactName': inn.get({'BOTSID': 'ST'},
                                    {'BOTSID': 'PER', 'PER02': None})})
    out.put({'BOTSID': 'Header',
             'ContactEmail': inn.get({'BOTSID': 'ST'},
                                     {'BOTSID': 'PER', 'PER08': None})})
    out.put({'BOTSID': 'Header',
             'ContactPhone': inn.get({'BOTSID': 'ST'},
                                     {'BOTSID': 'PER', 'PER04': None})})
    out.put({'BOTSID': 'Header',
             'ContactFax': inn.get({'BOTSID': 'ST'},
                                   {'BOTSID': 'PER', 'PER06': None})})

    for poc in inn.getloop({'BOTSID': 'ST'}, {'BOTSID': 'POC'}):
        line = out.putloop({'BOTSID': 'Header'}, {'BOTSID': 'LineItem'})
        line.put({'BOTSID': 'LineItem',
                  'LineNumber': poc.get({'BOTSID': 'POC', 'POC01': None})})
        line.put({'BOTSID': 'LineItem',
                  'ChangeCode': poc.get({'BOTSID': 'POC', 'POC02': None})})
        line.put({'BOTSID': 'LineItem',
                  'QuantityOrdered': poc.get({'BOTSID': 'POC', 'POC03': None})})
        line.put({'BOTSID': 'LineItem',
                  'UnitPrice': poc.get({'BOTSID': 'POC', 'POC06': None})})
        line.put({'BOTSID': 'LineItem',
                  'UnitPriceCode': poc.get({'BOTSID': 'POC', 'POC07': None})})
        line.put({'BOTSID': 'LineItem',
                  'ISBN': poc.get({'BOTSID': 'POC', 'POC09': None})})
        line.put({'BOTSID': 'LineItem',
                  'StudentEdition': poc.get({'BOTSID': 'POC', 'POC11': None})})
        line.put({'BOTSID': 'LineItem',
                  'StudentEditionCost': poc.get({'BOTSID': 'POC', 'POC13': None})})
        line.put({'BOTSID': 'LineItem',
                  'SchoolDistrictOwes': poc.get({'BOTSID': 'POC', 'POC15': None})})
