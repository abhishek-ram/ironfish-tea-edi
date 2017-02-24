from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import PurchaseOrder, PurchaseOrderLine, Watcher
from .models import School, SalesPerson, ShippingInvoice
from .utils import GPWebService
from .serializers import ShippingInvoiceSerializer
from decimal import Decimal


class CRUDPurchaseOrder(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request):
        """Endpoint for creating new purchase orders"""
        po = PurchaseOrder(
            order_id='TEA%s' % request.data['Header']['OrderNumber'],
            order_date=request.data['Header']['OrderDate'],
            customer_po=request.data['Header']['OrderNumber'],
            batch_id='TEA%s' % request.data['Header']['BatchNumber'],
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
                school = School.objects.filter(
                    isd_code=address['Code'].lstrip('0')).first()
                if school:
                    po.sales_id = school.sales_id
                    salesperson = SalesPerson.objects.filter(
                        school=school).first()
                    if salesperson:
                        po.salesperson = salesperson.name
        po.save()

        gp_ws_client = GPWebService()
        order_total, order_total_extra = 0, 0
        for line in request.data['Header']['LineItem']:
            line_total = Decimal(
                line['UnitPrice']) * Decimal(line['QuantityOrdered'])
            order_total += line_total
            order_total_extra += (
                line_total + Decimal(line['SchoolDistrictOwes']))

            gp_item_info = gp_ws_client.get_item_by_id(line['ISBN'])
            if 'ICEV' in gp_item_info['Description'].upper():
                po.is_ICEV = True

            PurchaseOrderLine.objects.create(
                purchase_order=po,
                sequence=line['LineNumber'],
                quantity=line['QuantityOrdered'],
                quantity_uom='EA',
                unit_price=line['UnitPrice'],
                unit_price_code=line['UnitPriceCode'],
                sub_total=line_total,
                ship_date=po.ship_date,
                isbn=line['ISBN'],
                description=gp_item_info['Description'],
                student_edition=line['StudentEdition'],
                student_edition_cost=line['StudentEditionCost'],
                school_district_owes=line['SchoolDistrictOwes']
            )

        po.owed_by_isd = order_total
        po.extra = order_total_extra

        po.save()

        # Notify any watchers that are listening for New POs
        watchers = [w.email_id for w in
                    Watcher.objects.filter(events__contains='PO_NEW')]
        if watchers:
            email_body = render_to_string(
                'emails/purchaseorder_new.html', {'po': po})
            send_mail('[TEAEDI] New Purchase Order Notification',
                      from_email='',
                      recipient_list=watchers,
                      message='',
                      html_message=email_body)
        return Response({'status': 'OK', 'id': po.pk})

    def put(self, request):
        """Endpoint for updating existing purchase orders"""

        # Fetch the original PO from the DB
        po = PurchaseOrder.objects.get(
            request=request.data['Header']['OrderNumber'], pk=null)

        # If PO exists go process each line in the PO change
        email_context = {
            'po': po,
            'changed_lines': [],
            'deleted_lines': [],
            'added_lines': []
        }
        for line in request.data['Header']['LineItem']:
            # Look for the line item in the original PO
            po_line = PurchaseOrderLine.objects.filter(
                purchase_order=po, isbn=line['ISBN']).first()
            if not po_line:
                line_total = Decimal(
                    line['UnitPrice']) * Decimal(line['QuantityOrdered'])
                po_line = PurchaseOrderLine(
                    purchase_order=po,
                    sequence=line['LineNumber'],
                    quantity=line['QuantityOrdered'],
                    quantity_uom='EA',
                    unit_price=line['UnitPrice'],
                    unit_price_code=line['UnitPriceCode'],
                    sub_total=line_total,
                    ship_date=po.ship_date,
                    isbn=line['ISBN'],
                    student_edition=line['StudentEdition'],
                    student_edition_cost=line['StudentEditionCost'],
                    school_district_owes=line['SchoolDistrictOwes']
                )

            if line['ChangeCode'] == 'DI':
                po.order_status = 'M'
                po_line.cancelled = True
                po_line.sub_total = 0
                po_line.save()
                email_context['deleted_lines'].append(po_line)
            elif line['ChangeCode'] == 'CA':
                po.order_status = 'M'
                po_line.original_quantity = po_line.quantity
                po_line.quantity = line['QuantityOrdered']
                po_line.sub_total = Decimal(
                    line['UnitPrice']) * Decimal(line['QuantityOrdered'])
                po_line.modified = True
                po_line.save()
                email_context['changed_lines'].append(po_line)
            elif line['ChangeCode'] == 'AI':
                po.order_status = 'M'
                po_line.added = True
                po_line.save()
                email_context['added_lines'].append(po_line)

        # Recalculate the total PO amount
        po.owed_by_isd = reduce(
            lambda x, y: x + y, [l.sub_total for l in po.lines.all()])

        # If all items have been cancelled mark PO as cancelled
        for line in po.lines.all():
            if not line.cancelled:
                break
        else:
            po.order_status = 'C'
        po.save()

        # Notify any watchers that are listening for PO Changes
        watchers = [w.email_id for w in
                    Watcher.objects.filter(events__contains='PO_UPD')]
        if watchers:
            email_body = render_to_string(
                'emails/purchaseorder_change.html', email_context)
            send_mail('[TEAEDI] Purchase Order Change Notification',
                      from_email='',
                      recipient_list=watchers,
                      message='',
                      html_message=email_body)
        return Response({'status': 'OK'})


class ShippingInvoiceList(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = ShippingInvoice.objects.filter(invoice_status='RP')
    serializer_class = ShippingInvoiceSerializer


class ShippingInvoiceMarkProcessed(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        """Endpoint for marking Shipping Invoices as processed"""

        # Get the shipping invoice object and update its status
        shipping_invoice = get_object_or_404(ShippingInvoice, pk=pk)
        shipping_invoice.invoice_status = 'P'
        shipping_invoice.save()

        # Notify any watchers that are listening for SI Processed
        watchers = [w.email_id for w in
                    Watcher.objects.filter(events__contains='SI_PRO')]
        if watchers:
            email_body = render_to_string(
                'emails/shippinginvoice_processed.html',
                {'si': shipping_invoice}
            )
            send_mail('[TEAEDI] Shipping Invoice Processed Notification',
                      from_email='',
                      recipient_list=watchers,
                      message='',
                      html_message=email_body)
        return Response({'status': 'OK'})


class ProcessAcknowledgment(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    ACK_ERROR_CODES = {
        '1': 'Transaction set not supported',
        '2': 'Transaction set trailer missing',
        '3': 'Transaction set control number in header and '
             'trailer do not match',
        '4': 'Number of included segments does not match actual count',
        '5': 'One or more segments in error',
        '6': 'Missing or invalid transaction set identifier',
        '7': 'Missing or invalid transaction set control number '
             '(a duplicate transaction number may have occurred)'
    }

    def post(self, request):
        """Endpoint for processing received EDI acknowledgments from TEA"""

        for transaction in request.data['Group']['Transaction']:
            if transaction['Code'] == '857':
                si = ShippingInvoice.objects.get(request=transaction['Number'],
                                                 pk=transaction['Number'])
                si.invoice_status = transaction['Status']
                si.save()

                # Notify any watchers that are listening for SI Acknowledgments
                watchers = [w.email_id for w in
                            Watcher.objects.filter(events__contains='SI_ACK')]
                if watchers:
                    email_body = (
                        'Shipping invoice %s has been acknowledged by TEA with'
                        ' status "%s".') % (transaction['Number'],
                                            si.get_invoice_status_display())
                    if transaction.get('AdvStatus'):
                        email_body += (
                            '\nReason for the error is "%s". Please contact '
                            'the administrator for assistance in resolving the'
                            ' issue.') % self.ACK_ERROR_CODES[transaction['AdvStatus']]

                    send_mail(
                        '[TEAEDI] Shipping Invoice Acknowledgment Notification',
                        from_email='', recipient_list=watchers,
                        message=email_body
                    )
        return Response({'status': 'OK'})
