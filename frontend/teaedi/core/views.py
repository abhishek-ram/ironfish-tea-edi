from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from .models import PurchaseOrder, PurchaseOrderLine


@login_required()
def index(request):
    return render(request, 'core/index.html')


class CreatePurchaseOrder(APIView):
    authentication_classes = (TokenAuthentication,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        ship_to_name, ship_to_id = None, None
        for address in request.data['Header']['Address']:
            if address['AddressType'] == 'ST':
                ship_to_name = address['Name']
                ship_to_id = address['Code']
        po = PurchaseOrder.objects.create(
            order_id='TEA%s' % request.data['Header']['OrderNumber'],
            external_order_id=request.data['Header']['OrderNumber'],
            order_date=request.data['Header']['OrderDate'],
            requisition_id=request.data['Header']['RequisitionNumber'],
            ship_earliest=request.data['Header'].get('RequestedShipEarliest'),
            ship_latest=request.data['Header'].get('RequestedShipLatest'),
            ship_to_name=ship_to_name,
            ship_to_id=ship_to_id
        )
        for line in request.data['Header']['LineItem']:
            PurchaseOrderLine.objects.create(
                purchase_order=po,
                line_number=line['LineNumber'],
                quantity=line['QuantityOrdered'],
                quantity_uom=line['QuantityUOM'],
                unit_price=line['UnitPrice'],
                isbn=line['ISBN'],
                student_edition=line['StudentEdition'],
                student_edition_cost=line['StudentEditionCost'],
                school_district_owes=line['SchoolDistrictOwes']
            )
        return Response({'status': 'OK', 'id': po.pk})
