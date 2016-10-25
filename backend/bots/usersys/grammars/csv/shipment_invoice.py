from bots.botsconfig import *


syntax = {
    'field_sep': ',',
    'quote_char': '"'
}

structure= [
    {ID:'Header', MIN:1, MAX:1,
        QUERIES:{
            'frompartner': {'BOTSID':'Header','SenderId':None},
            'topartner': {'BOTSID':'Header','ReceiverId':None},
            'botskey': {'BOTSID':'Header','InvoiceNumber':None},
        },
        LEVEL:[
           {ID:'LineItem',MIN:1,MAX:10000},
        ]
     }
]

nextmessage = ({'BOTSID':'Header'},)

recorddefs = {
    'Header': [
        ['BOTSID', 'M', 20, 'A'],
        ['SenderId', 'M', 35, 'AN'],
        ['ReceiverId', 'M', 35, 'AN'],
        ['InvoiceNumber', 'M', 35, 'AN'],
        ['InvoiceDate', 'M', (8,8), 'D'],
        ['TotalBoxes', 'C', 10, 'R'],
        ['TotalWeight', 'C', 10, 'R'],
        ['FOBCharge', 'C', 10, 'R'],
        ['FreightBillNo', 'C', 35, 'AN'],
        ['ShipToName', 'C', 70, 'AN'],
        ['ShipToCode', 'C', 35, 'AN'],
        ['TotalCharge', 'C', 10, 'R'],
        ['OrderNumber', 'M', 35, 'AN'],
        ['OrderSequence', 'C', 10, 'N'],
        ['OrderDate', 'M', (8,8), 'D'],
        ['RequisitionNumber', 'C', 35, 'AN'],
    ],
    'LineItem': [
        ['BOTSID', 'M', 20, 'A'],
        ['LineNumber', 'M', 20, 'AN'],
        ['UnitPrice', 'M', 17, 'R'],
        ['ISBN', 'M', 48, 'AN'],
        ['StudentEdition', 'C', 48, 'AN'],
        ['StudentEditionCost', 'C', 48, 'AN'],
        ['Quantity', 'M', 9, 'R'],
        ['QuantityUOM', 'C', 10, 'AN'],
        ['ShippedDate', 'M', (8,8), 'D'],
    ],
}