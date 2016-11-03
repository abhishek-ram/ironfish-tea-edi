from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from .models import PurchaseOrder, PurchaseOrderLine
from decimal import Decimal


class CreatePurchaseOrder(APIView):
    authentication_classes = (TokenAuthentication,)
    parser_classes = (JSONParser,)

    def post(self, request, format=None):
        po = PurchaseOrder(
            order_id='TEA%s' % request.data['Header']['OrderNumber'],
            order_date=request.data['Header']['OrderDate'],
            customer_po=request.data['Header']['OrderNumber'],
            contract=request.data['Header']['RequisitionNumber'],
        )
        po.ship_date = \
            request.data['Header'].get('RequestedShipLatest') or \
            request.data['Header'].get('RequestedShipEarliest')

        for address in request.data['Header']['Address']:
            if address['AddressType'] == 'ST':
                po.isd_name = address['Name']
                po.isd_code = address['Code']
                po.address_line1 = address['AddressLine1']
                if address.get('AddressLine2'):
                    po.address_line2 = address['AddressLine1']
                po.city = address['City']
                po.state = address['StateCode']
                po.zip = address['PostalCode']
                po.contact_name = address['ContactName']
                po.contact_phone = address['ContactPhone']
                po.contact_email = address['ContactEmail']
                po.contact_fax = address['ContactFax']
        po.save()

        order_total, order_total_extra = 0, 0
        for line in request.data['Header']['LineItem']:
            line_total = Decimal(
                line['UnitPrice']) * Decimal(line['QuantityOrdered'])
            order_total += line_total
            order_total_extra += (
                line_total + Decimal(line['SchoolDistrictOwes']))

            PurchaseOrderLine.objects.create(
                purchase_order=po,
                sequence=line['LineNumber'],
                quantity=line['QuantityOrdered'],
                quantity_uom=line['QuantityUOM'],
                unit_price=line['UnitPrice'],
                unit_price_code=line['UnitPriceCode'],
                total_price=line_total,
                ship_date=po.ship_date,
                isbn=line['ISBN'],
                student_edition=line['StudentEdition'],
                student_edition_cost=line['StudentEditionCost'],
                school_district_owes=line['SchoolDistrictOwes']
            )

        po.owed_by_isd = order_total
        po.extra = order_total_extra
        po.save()
        return Response({'status': 'OK', 'id': po.pk})