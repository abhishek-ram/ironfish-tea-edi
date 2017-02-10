from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from ....core.utils import GPWebService
from ....core.models import ShippingInvoice, ShippingInvoiceLine, \
    PurchaseOrder, PurchaseOrderLine
import logging

logger = logging.getLogger('teaedi')


class Command(BaseCommand):
    help = 'Import orders from GP into the front end'

    @transaction.atomic
    def handle(self, *args, **options):
        gp_ws = GPWebService()
        for invoice in gp_ws.get_invoice_list('7TEX701'):
            invoice_id = invoice['Key']['Id']
            logger.info('Begin import of invoice {} from GP'.format(
                invoice_id))
            if ShippingInvoice.objects.filter(pk=invoice_id).exists():
                logger.info('Invoice {} already imported, skipping it.'.format(
                    invoice_id))
                continue

            logger.info('Fetch detailed information for invoice {}'.format(
                invoice_id))
            invoice_details = gp_ws.get_invoice_detail(invoice_id)

            purchase_order = PurchaseOrder.objects.filter(pk=invoice_details[
                'OriginalSalesDocumentKey']['Id']).first()

            if not purchase_order:
                logger.error('Related PO not found for  {}. Skip it.'.format(
                    invoice_id))

            logger.info('Importing invoice {} into the frontend.'.format(
                invoice_id))
            shipping_invoice = ShippingInvoice.objects.create(
                purchase_order=purchase_order,
                invoice_id=invoice_id,
                invoice_date=invoice_details['InvoiceDate'],
                actual_ship_date=invoice_details['InvoiceDate'],
                # actual_ship_date=invoice_details['UserDefined']['Date01'],
                boxes=invoice_details['UserDefined']['List01'] or 0,
                weight=invoice_details['UserDefined']['Text01'] or 0,
                shipping_cost=invoice_details['UserDefined']['List02'] or 0,
                tracking_number=invoice_details['UserDefined']['Text05'] or 0,
                total_amount=invoice_details['TotalAmount']['Value']
            )

            for line in invoice_details['Lines']['SalesInvoiceLine']:
                isbn = line['ItemKey']['Id']
                quantity = line['Quantity']['Value']
                po_line = PurchaseOrderLine.objects.get(
                    purchase_order=purchase_order, isbn=isbn, quantity=quantity)
                # Create the shipping invoice line object.
                ShippingInvoiceLine.objects.create(
                    shipping_invoice=shipping_invoice,
                    sequence=po_line.sequence,
                    quantity=quantity,
                    quantity_uom=po_line.quantity_uom,
                    unit_price=line['UnitPrice']['Value'],
                    total_amount=line['TotalAmount']['Value'],
                    isbn=isbn,
                    description=line['ItemDescription'],
                    actual_ship_date=invoice_details['UserDefined']['Date01'],
                    student_edition=po_line.student_edition,
                    student_edition_cost=po_line.student_edition_cost,
                    school_district_owes=po_line.student_edition_cost,
                )

            logger.info('End import of invoice {} from GP.'.format(
                invoice_id))