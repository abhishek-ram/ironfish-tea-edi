import bots.transform as transform


def main(inn, out):
    out.put({'BOTSID': 'ST',
             'ST01': '857',
             'ST02': out.ta_info['reference'].zfill(4)
             })
    out.put({'BOTSID': 'ST'}, {'BOTSID': 'BHT',
                               'BHT01': '0001',
                               'BHT02': '00',
                               'BHT03': inn.ta_info['botskey'],
                               'BHT06': 'AB'
                               })

    doc_date = inn.get({'BOTSID': 'Header', 'InvoiceDate': None})
    out.put({'BOTSID': 'ST'}, {'BOTSID': 'BHT',
                               'BHT04': transform.datemask(doc_date, 'CCYYMMDD', 'YYMMDD')
                               })

    ship_hl = out.putloop({'BOTSID': 'ST'}, {'BOTSID': 'HL'})
    ship_hl.put({'BOTSID': 'HL', 'HL01': '1', 'HL03': 'S', 'HL04': '1'})
    ship_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'G05',
                                   'G0501': inn.get({'BOTSID': 'Header',
                                                     'TotalBoxes': None}),
                                   'G0502': 'BX'})
    ship_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'G05',
                                   'G0503': inn.get({'BOTSID': 'Header',
                                                     'TotalWeight': None}),
                                   'G0504': '01'})
    ship_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'G05',
                                   'G0505': inn.get({'BOTSID': 'Header',
                                                     'TotalBoxes': None}),
                                   'G0506': 'PL'})

    ship_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'G05'},
                {'BOTSID': 'FOB',
                 'FOB01': 'PS',
                 'FOB09': inn.get({'BOTSID': 'Header', 'FOBCharge': None})})

    ship_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'G05'},
                {'BOTSID': 'DTM',
                 'DTM01': '011',
                 'DTM02': transform.datemask(doc_date, 'CCYYMMDD', 'YYMMDD'),
                 'DTM05': transform.datemask(doc_date, 'CCYYMMDD', 'CC')
                 })

    ship_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'G05'},
                {'BOTSID': 'N9',
                 'N901': 'FR',
                 'N902': inn.get({'BOTSID': 'Header', 'FreightBillNo': None})})

    ship_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'G05'},
                {'BOTSID': 'N1',
                 'N101': 'ST',
                 'N102': inn.get({'BOTSID': 'Header', 'ShipToName': None}),
                 'N103': '76',
                 'N104': inn.get({'BOTSID': 'Header', 'ShipToCode': None})
                 })

    order_hl = out.putloop({'BOTSID': 'ST'}, {'BOTSID': 'HL'})
    order_hl.put({'BOTSID': 'HL', 'HL01': '2', 'HL03': 'O', 'HL04': '1'})

    order_hl.put({'BOTSID': 'HL'},
                 {'BOTSID': 'TDS',
                  'TDS01': inn.get({'BOTSID': 'Header', 'TotalCharge': None})})

    order_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'TDS'},
                 {'BOTSID': 'PRF',
                  'PRF01': inn.get({'BOTSID': 'Header', 'OrderNumber': None})})
    order_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'TDS'},
                 {'BOTSID': 'PRF',
                  'PRF03': inn.get({'BOTSID': 'Header', 'OrderSequence': None})})

    ord_date = inn.get({'BOTSID': 'Header', 'OrderDate': None})
    order_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'TDS'},
                 {'BOTSID': 'PRF',
                  'PRF04': transform.datemask(ord_date, 'CCYYMMDD', 'YYMMDD')})

    order_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'TDS'},
                 {'BOTSID': 'PRF',
                  'PRF05': inn.get({'BOTSID': 'Header', 'ShipToCode': None})})
    order_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'TDS'},
                 {'BOTSID': 'PRF',
                  'PRF06': inn.get({'BOTSID': 'Header', 'RequisitionNumber': None})})

    order_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'TDS'},
                 {'BOTSID': 'N9',
                  'N901': 'IK',
                  'N902': inn.ta_info['botskey']})

    hl_count = 3
    for line in inn.getloop({'BOTSID': 'Header'}, {'BOTSID': 'LineItem'}):
        line_hl = out.putloop({'BOTSID': 'ST'}, {'BOTSID': 'HL'})
        line_hl.put({'BOTSID': 'HL', 'HL01': hl_count, 'HL03': 'I', 'HL04': '0'})
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT101': line.get({'BOTSID': 'LineItem', 'LineNumber': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT103': 'UN',
                     'IT102': line.get({'BOTSID': 'LineItem', 'Quantity': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT105': '03',
                     'IT104': line.get({'BOTSID': 'LineItem', 'UnitPrice': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT106': 'IB',
                     'IT107': line.get({'BOTSID': 'LineItem', 'ISBN': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT108': 'SE',
                     'IT109': line.get({'BOTSID': 'LineItem', 'StudentEdition': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT110': 'SC',
                     'IT111': line.get({'BOTSID': 'LineItem', 'StudentEditionCost': None})
                     })
        line_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'IT1'},
                    {'BOTSID': 'IT3',
                     'IT301': line.get({'BOTSID': 'LineItem', 'Quantity': None}),
                     'IT302': line.get({'BOTSID': 'LineItem', 'QuantityUOM': None}),
                     'IT303': 'SH',
                     'IT304': '0'
                     })
        ship_date = line.get({'BOTSID': 'LineItem', 'ShippedDate': None})
        line_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'IT1'},
                    {'BOTSID': 'DTM',
                     'DTM01': '011',
                     'DTM02': transform.datemask(ship_date, 'CCYYMMDD', 'YYMMDD'),
                     'DTM05': transform.datemask(ship_date, 'CCYYMMDD', 'CC')
                     })
        line_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'IT1'},
                    {'BOTSID': 'SAC', 'SAC01': 'C', 'SAC05': '0'})

        hl_count += 1

    out.put({'BOTSID': 'ST'}, {'BOTSID': 'SE',
                               'SE01': out.getcount()+1,
                               'SE02': out.ta_info['reference'].zfill(4)
                               })

