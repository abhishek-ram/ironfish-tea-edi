from bots.botsconfig import *


syntax = {
    'indented': True,
    'merge': False
}

structure = [
    {ID:'Group',MIN:1,MAX:1,LEVEL:[
        {ID:'Transaction',MIN:1,MAX:9999,LEVEL:[
            {ID:'Error',MIN:0,MAX:99}
        ]},
    ]}
]

recorddefs = {
    'Group':[
        ['BOTSID','M',20,'A'],
        ['SenderId', 'M', 35, 'AN'],
        ['ReceiverId', 'M', 35, 'AN'],
        ['Code', 'M', 2, 'AN'],
        ['Status', 'M', 1, 'AN'],
        ['AdvStatus', 'C', 3, 'AN'],
    ],
    'Transaction': [
        ['BOTSID', 'M', 20, 'A'],
        ['Code', 'M', 3, 'AN'],
        ['Number', 'M', 9, 'AN'],
        ['Status', 'M', 2, 'AN'],
        ['AdvStatus', 'C', 3, 'AN'],
    ],
    'Error': [
        ['BOTSID', 'M', 20, 'A'],
        ['SegmentCode', 'M', 3, 'AN'],
        ['SegmentPosition', 'M', 6, 'AN'],
        ['SegmentError', 'C', 3, 'AN'],
        ['DataPosition1', 'M', 2, 'AN'],
        ['DataPosition2', 'C', 2, 'AN'],
        ['DataError', 'M', 3, 'AN'],
        ['DataCopy', 'C', 99, 'AN'],
    ]
}
