from bots.botsconfig import *


syntax = {
    'indented': True,
    'merge': False
}

structure = [
    {ID:'Header',MIN:1,MAX:1,LEVEL:[
        {ID:'LineItem',MIN:1,MAX:9999},
    ]}
]

recorddefs = {
    'Header':[
        ['BOTSID','M',10,'A'],
        ['SenderId', 'M', 35, 'AN'],
        ['ReceiverId', 'M', 35, 'AN'],
        ['OrderType', 'M', 3, 'AN'],
        ['OrderNumber', 'M', 35, 'AN'],
        ['OrderDate', 'M', (8,8), 'D'],
        ['ChangeOrderSeq', 'M', 8, 'AN'],
        ['ContactName', 'C', 60, 'AN'],
        ['ContactEmail', 'C', 80, 'AN'],
        ['ContactPhone', 'C', 80, 'AN'],
        ['ContactFax', 'C', 80, 'AN'],
    ],
    'LineItem': [
        ['BOTSID', 'M', 10, 'A'],
        ['LineNumber', 'M', 20, 'AN'],
        ['ChangeCode', 'M', 20, 'AN'],
        ['QuantityOrdered', 'M', 9, 'R'],
        ['QuantityUOM', 'C', 2, 'AN'],
        ['UnitPrice', 'M', 17, 'R'],
        ['UnitPriceCode', 'C', 2, 'AN'],
        ['ISBN', 'M', 48, 'AN'],
        ['StudentEdition', 'C', 48, 'AN'],
        ['StudentEditionCost', 'C', 48, 'AN'],
        ['SchoolDistrictOwes', 'C', 48, 'AN'],
    ],
}
