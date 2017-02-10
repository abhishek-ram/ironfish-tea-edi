from bots.botsconfig import *

structure= [
    {ID:'Invoice', MIN:1, MAX:1,
        QUERIES:{
            'botskey': {'BOTSID':'Invoice','invoice_id':None},
        },
        LEVEL:[
           {ID:'Lines',MIN:1,MAX:10000},
        ]
     }
]

recorddefs = {
    'Invoice': [
        ['BOTSID', 'M', 20, 'A'],
        ['invoice_id', 'M', 35, 'AN'],
        ['invoice_date', 'C', 256, 'AN'],
        ['actual_ship_date', 'C', 256, 'AN'],
        ['purchase_order', 'C', 256, 'AN'],
        ['purchase_order_date', 'C', 256, 'AN'],
        ['contract', 'C', 256, 'AN'],
        ['invoice_status', 'C', 10, 'AN'],
        ['isd_name', 'C', 2560, 'AN'],
        ['isd_code', 'C', 256, 'AN'],
        ['carrier_name', 'C', 256, 'AN'],
        ['carrier_code', 'C', 256, 'AN'],
        ['boxes', 'C', 256, 'AN'],
        ['weight', 'C', 256, 'AN'],
        ['shipping_cost', 'C', 256, 'AN'],
        ['tracking_number', 'C', 256, 'AN'],
        ['total_amount', 'C', 256, 'AN'],
    ],
    'Lines': [
        ['BOTSID', 'M', 20, 'A'],
        ['sequence', 'C', 256, 'AN'],
        ['quantity', 'C', 256, 'AN'],
        ['quantity_uom', 'C', 256, 'AN'],
        ['unit_price', 'C', 256, 'AN'],
        ['total_amount', 'C', 256, 'AN'],
        ['actual_ship_date', 'C', 256, 'AN'],
        ['isbn', 'C', 256, 'AN'],
        ['description', 'C', 256, 'AN'],
        ['student_edition', 'C', 256, 'AN'],
        ['student_edition_cost', 'C', 256, 'AN'],
        ['school_district_owes', 'C', 256, 'AN'],
    ],
}