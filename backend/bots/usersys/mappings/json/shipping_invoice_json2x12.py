import bots.transform as transform


def main(inn, out):
    out.put({'BOTSID': 'ST',
             'ST01': '857',
             'ST02': out.ta_info['reference'].zfill(4)
             })
    out.put({'BOTSID': 'ST'}, 
            {'BOTSID': 'BHT',
             'BHT01': '0001',
             'BHT02': '00',
             'BHT03': inn.ta_info['botskey'],
             'BHT06': 'AB'
             })

    doc_date = inn.get({'BOTSID': 'Invoice', 'actual_ship_date': None})
    out.put({'BOTSID': 'ST'},
            {'BOTSID': 'BHT',
             'BHT04': transform.datemask(doc_date, 'CCYY-MM-DD', 'YYMMDD')
             })

    ship_hl = out.putloop({'BOTSID': 'ST'}, {'BOTSID': 'HL'})
    ship_hl.put({'BOTSID': 'HL', 'HL01': '1', 'HL03': 'S', 'HL04': '1'})

    ship_hl.put({'BOTSID': 'HL'},
                {'BOTSID': 'G05',
                 'G0501': inn.get({'BOTSID': 'Invoice', 'boxes': None}),
                 'G0502': 'BX',
                 'G0503': inn.get({'BOTSID': 'Invoice', 'weight': None}),
                 'G0504': '01',
                 'G0505': '1',
                 'G0506': 'PL'
                 })

    ship_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'G05'},
                {'BOTSID': 'FOB',
                 'FOB01': 'PS',
                 'FOB09': inn.get({'BOTSID': 'Invoice', 'shipping_cost': None})
                 })

    ship_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'G05'},
                {'BOTSID': 'DTM',
                 'DTM01': '011',
                 'DTM02': transform.datemask(doc_date, 'CCYY-MM-DD', 'YYMMDD'),
                 'DTM05': transform.datemask(doc_date, 'CCYY-MM-DD', 'CC')
                 })

    ship_hl.put({'BOTSID': 'HL'},
                {'BOTSID': 'G05'},
                {'BOTSID': 'N9',
                 'N901': 'FR',
                 'N902': inn.get({'BOTSID': 'Invoice', 'tracking_number': None})
                 })

    ship_hl.put({'BOTSID': 'HL'},
                {'BOTSID': 'G05'},
                {'BOTSID': 'N1',
                 'N101': 'ST',
                 'N102': inn.get({'BOTSID': 'Invoice', 'isd_name': None}),
                 'N103': '76',
                 'N104': inn.get({'BOTSID': 'Invoice', 'isd_code': None})
                 })

    ship_hl.put({'BOTSID': 'HL'},
                {'BOTSID': 'G05'},
                {'BOTSID': 'N1',
                 'N101': 'CA',
                 'N102': inn.get({'BOTSID': 'Invoice', 'carrier_name': None}),
                 'N103': '75',
                 'N104': inn.get({'BOTSID': 'Invoice', 'carrier_code': None})
                 })

    order_hl = out.putloop({'BOTSID': 'ST'}, {'BOTSID': 'HL'})
    order_hl.put({'BOTSID': 'HL', 'HL01': '2', 'HL03': 'O', 'HL04': '1'})

    order_hl.put({'BOTSID': 'HL'},
                 {'BOTSID': 'TDS',
                  'TDS01': inn.get({'BOTSID': 'Invoice', 'total_amount': None})
                  })

    ord_date = inn.get({'BOTSID': 'Invoice', 'purchase_order_date': None})

    order_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'TDS'},
                 {'BOTSID': 'PRF',
                  'PRF01': inn.get({'BOTSID': 'Invoice', 'purchase_order': None}),
                  'PRF03': '0',
                  'PRF04': transform.datemask(ord_date, 'CCYY-MM-DD', 'YYMMDD'),
                  'PRF05': inn.get({'BOTSID': 'Invoice', 'isd_code': None}),
                  'PRF06': inn.get({'BOTSID': 'Invoice', 'contract': None})
                  })

    order_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'TDS'},
                 {'BOTSID': 'N9',
                  'N901': 'IK',
                  'N902': inn.ta_info['botskey']})

    hl_count = 3
    for line in inn.getloop({'BOTSID': 'Invoice'}, {'BOTSID': 'Lines'}):
        line_hl = out.putloop({'BOTSID': 'ST'}, {'BOTSID': 'HL'})
        line_hl.put({'BOTSID': 'HL', 'HL01': hl_count, 'HL03': 'I', 'HL04': '0'})
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT101': line.get({'BOTSID': 'Lines', 'sequence': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT103': 'UN',
                     'IT102': line.get({'BOTSID': 'Lines', 'quantity': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT105': '03',
                     'IT104': line.get({'BOTSID': 'Lines', 'unit_price': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT106': 'IB',
                     'IT107': line.get({'BOTSID': 'Lines', 'isbn': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT108': 'SE',
                     'IT109': line.get({'BOTSID': 'Lines',
                                        'student_edition': None})
                     })
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1',
                     'IT110': 'SC',
                     'IT111': line.get({'BOTSID': 'Lines',
                                        'student_edition_cost': None})
                     })

        line_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'IT1'},
                    {'BOTSID': 'IT3',
                     'IT301': line.get({'BOTSID': 'Lines', 'quantity': None}),
                     'IT302': line.get({'BOTSID': 'Lines', 'quantity_uom': None}),
                     'IT303': 'SH',
                     'IT304': '0'
                     })

        ship_date = line.get({'BOTSID': 'Lines', 'actual_ship_date': None})
        line_hl.put({'BOTSID': 'HL'},
                    {'BOTSID': 'IT1'},
                    {'BOTSID': 'DTM',
                     'DTM01': '011',
                     'DTM02': transform.datemask(ship_date, 'CCYY-MM-DD', 'YYMMDD'),
                     'DTM05': transform.datemask(ship_date, 'CCYY-MM-DD', 'CC')
                     })

        line_hl.put({'BOTSID': 'HL'}, {'BOTSID': 'IT1'},
                    {'BOTSID': 'SAC',
                     'SAC01': 'C',
                     'SAC02': 'ZZZZ',
                     'SAC05': line.get({'BOTSID': 'Lines', 'total_amount': None}),
                     })

        hl_count += 1

    out.put({'BOTSID': 'ST'}, {'BOTSID': 'SE',
                               'SE01': out.getcount()+1,
                               'SE02': out.ta_info['reference'].zfill(4)
                               })

