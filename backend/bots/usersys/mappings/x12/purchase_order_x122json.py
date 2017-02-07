import bots.transform as transform


def main(inn, out):
    out.put({'BOTSID': 'Header', 'SenderId': inn.ta_info['frompartner']})
    out.put({'BOTSID': 'Header', 'ReceiverId': inn.ta_info['topartner']})
    out.put({'BOTSID': 'Header',
             'OrderType': inn.get({'BOTSID': 'ST'},
                                  {'BOTSID': 'BEG', 'BEG02': None})})

    doc_num = inn.get({'BOTSID': 'ST'}, {'BOTSID': 'BEG', 'BEG03': None})
    inn.ta_info['botskey'] = out.ta_info['botskey'] = doc_num
    out.put({'BOTSID': 'Header', 'OrderNumber': doc_num})

    order_date = inn.get({'BOTSID': 'ST'}, {'BOTSID': 'BEG', 'BEG05.02': None}) + \
                 inn.get({'BOTSID': 'ST'}, {'BOTSID': 'BEG', 'BEG05.01': None})
    out.put({'BOTSID': 'Header',
             'OrderDate': transform.datemask(
                 order_date, 'YYYYMMDD', 'YYYY-MM-DD')})

    out.put({'BOTSID': 'Header',
             'RequisitionNumber': inn.get({'BOTSID': 'ST'},
                                          {'BOTSID': 'BEG', 'BEG06': None})})
    out.put({'BOTSID': 'Header',
             'BatchNumber':
                 transform.datemask(
                     order_date, 'CCYYMMDD', 'MMDDYY') +
                 inn.ta_info['bots_accessenvelope'].children[0].get(
                     {'BOTSID': 'ISA', 'ISA10': None})
             })
    ship_date_begin = inn.get({'BOTSID': 'ST'},
                              {'BOTSID': 'DTM', 'DTM01': '010', 'DTM02': None})
    ship_date_begin_ce = inn.get({'BOTSID': 'ST'},
                                 {'BOTSID': 'DTM', 'DTM01': '010', 'DTM05': None})

    if ship_date_begin and ship_date_begin_ce:
        out.put({'BOTSID': 'Header',
                 'RequestedShipEarliest': transform.datemask(
                     ship_date_begin_ce + ship_date_begin,
                     'YYYYMMDD',
                     'YYYY-MM-DD')
                 })

    ship_date_end = inn.get({'BOTSID': 'ST'},
                            {'BOTSID': 'DTM', 'DTM01': '084', 'DTM02': None})
    ship_date_end_ce = inn.get({'BOTSID': 'ST'},
                               {'BOTSID': 'DTM', 'DTM01': '084', 'DTM05': None})

    if ship_date_end and ship_date_end_ce:
        out.put({'BOTSID': 'Header',
                 'RequestedShipLatest': transform.datemask(
                     ship_date_end_ce + ship_date_end,
                     'YYYYMMDD',
                     'YYYY-MM-DD')
                 })

    for n1 in inn.getloop({'BOTSID': 'ST'}, {'BOTSID': 'N1'}):
        address = out.putloop({'BOTSID': 'Header'}, {'BOTSID': 'Address'})
        address.put({'BOTSID': 'Address',
                     'AddressType': n1.get({'BOTSID': 'N1', 'N101': None})})
        address.put({'BOTSID': 'Address',
                     'Name': n1.get({'BOTSID': 'N1', 'N102': None})})
        address.put({'BOTSID': 'Address',
                     'CodeQualifier': n1.get({'BOTSID': 'N1', 'N103': None})})
        address.put({'BOTSID': 'Address',
                     'Code': n1.get({'BOTSID': 'N1', 'N104': None})})
        address.put({'BOTSID': 'Address',
                     'DivisionName': n1.get({'BOTSID': 'N1'},
                                            {'BOTSID': 'N2', 'N201': None})})
        address.put({'BOTSID': 'Address',
                     'AddressLine1': n1.get({'BOTSID': 'N1'},
                                            {'BOTSID': 'N3', 'N301': None})})
        address.put({'BOTSID': 'Address',
                     'AddressLine2': n1.get({'BOTSID': 'N1'},
                                            {'BOTSID': 'N3', 'N302': None})})
        address.put({'BOTSID': 'Address',
                     'City': n1.get({'BOTSID': 'N1'},
                                    {'BOTSID': 'N4', 'N401': None})})
        address.put({'BOTSID': 'Address',
                     'StateCode': n1.get({'BOTSID': 'N1'},
                                         {'BOTSID': 'N4', 'N402': None})})
        address.put({'BOTSID': 'Address',
                     'PostalCode': n1.get({'BOTSID': 'N1'},
                                          {'BOTSID': 'N4', 'N403': None})})
        address.put({'BOTSID': 'Address',
                     'ContactName': n1.get({'BOTSID': 'N1'},
                                           {'BOTSID': 'PER', 'PER02': None})})
        address.put({'BOTSID': 'Address',
                     'ContactEmail': n1.get({'BOTSID': 'N1'},
                                            {'BOTSID': 'PER', 'PER08': None})})
        address.put({'BOTSID': 'Address',
                     'ContactPhone': n1.get({'BOTSID': 'N1'},
                                            {'BOTSID': 'PER', 'PER04': None})})
        address.put({'BOTSID': 'Address',
                     'ContactFax': n1.get({'BOTSID': 'N1'},
                                          {'BOTSID': 'PER', 'PER06': None})})

    for po1 in inn.getloop({'BOTSID': 'ST'}, {'BOTSID': 'PO1'}):
        line = out.putloop({'BOTSID': 'Header'}, {'BOTSID': 'LineItem'})
        line.put({'BOTSID': 'LineItem',
                  'LineNumber': po1.get({'BOTSID': 'PO1', 'PO101': None})})
        line.put({'BOTSID': 'LineItem',
                  'QuantityOrdered': po1.get({'BOTSID': 'PO1', 'PO102': None})})
        line.put({'BOTSID': 'LineItem',
                  'QuantityUOM': po1.get({'BOTSID': 'PO1', 'PO103': None})})
        line.put({'BOTSID': 'LineItem',
                  'UnitPrice': po1.get({'BOTSID': 'PO1', 'PO104': None})})
        line.put({'BOTSID': 'LineItem',
                  'UnitPriceCode': po1.get({'BOTSID': 'PO1', 'PO105': None})})
        line.put({'BOTSID': 'LineItem',
                  'ISBN': po1.get({'BOTSID': 'PO1', 'PO107': None})})
        line.put({'BOTSID': 'LineItem',
                  'StudentEdition': po1.get({'BOTSID': 'PO1', 'PO109': None})})
        line.put({'BOTSID': 'LineItem',
                  'StudentEditionCost': po1.get({'BOTSID': 'PO1', 'PO111': None})})
        line.put({'BOTSID': 'LineItem',
                  'SchoolDistrictOwes': po1.get({'BOTSID': 'PO1', 'PO113': None})})
