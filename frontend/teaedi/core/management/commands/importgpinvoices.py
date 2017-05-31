from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.core.mail import mail_admins
from ....core.utils import GPWebService
from ....core.models import ShippingInvoice, ShippingInvoiceLine, \
    PurchaseOrder, PurchaseOrderLine
import logging
import traceback

logger = logging.getLogger('teaedi')


class Command(BaseCommand):
    help = 'Import orders from GP into the front end'

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            gp_ws = GPWebService()
            for invoice in gp_ws.get_invoice_list('7TEX701'):
                invoice_id = invoice['Key']['Id']
                logger.info('Begin import of invoice {} from GP'.format(
                    invoice_id))

                if ShippingInvoice.objects.filter(pk=invoice_id).exists():
                    logger.info('Invoice {} already imported, '
                                'skipping it.'.format(invoice_id))
                    continue

                logger.info('Fetch detailed information for invoice {}'.format(
                    invoice_id))
                invoice_details = gp_ws.get_invoice_detail(invoice_id)

                if not invoice_details['BatchKey']['Id'].lower().startswith(
                        'transmit'):
                    logger.info('Invoice {} not ready for transmitting, '
                                'skipping it.'.format(invoice_id))
                    continue

                purchase_order = PurchaseOrder.objects.filter(
                    pk=invoice_details['OriginalSalesDocumentKey']['Id']).first()

                if not purchase_order:
                    logger.error('Related PO not found for  {}. '
                                 'Skipping it.'.format(invoice_id))

                logger.info('Importing invoice {} into the frontend.'.format(
                    invoice_id))
                ship_date = \
                    invoice_details['UserDefined']['Date01'] or \
                    timezone.localtime(timezone.now()).date()

                shipping_invoice = ShippingInvoice.objects.create(
                    purchase_order=purchase_order,
                    invoice_id=invoice_id,
                    invoice_date=ship_date,
                    actual_ship_date=ship_date,
                    boxes=invoice_details['UserDefined']['List01'] or 1,
                    weight=invoice_details['UserDefined']['Text01'] or 1,
                    shipping_cost=invoice_details['UserDefined']['List02'] or 0,
                    tracking_number=invoice_details['UserDefined'][
                                        'Text05'] or 0,
                    total_amount=invoice_details['TotalAmount']['Value']
                )

                added_sequences = []
                for line in invoice_details['Lines']['SalesInvoiceLine']:
                    isbn = line['ItemKey']['Id']
                    quantity = line['Quantity']['Value']
                    po_lines = PurchaseOrderLine.objects.filter(
                        purchase_order=purchase_order,
                        isbn=isbn,
                        quantity=quantity
                    )
                    po_line = None
                    for pl in po_lines:
                        if pl.sequence not in added_sequences:
                            po_line = pl
                            added_sequences.append(pl.sequence)
                            break

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
                        actual_ship_date=ship_date,
                        student_edition=po_line.student_edition,
                        student_edition_cost=po_line.student_edition_cost,
                        school_district_owes=po_line.student_edition_cost,
                    )

                logger.info('Completed import of invoice {} from GP.'.format(
                    invoice_id))

        except Exception:
            mail_admins(
                subject='Import GP Invoice Process Failed',
                message='Import GP Invoice process failed at {}, '
                        'cause of error is:\n {}'.format(timezone.now(),
                                                         traceback.format_exc())
            )
            raise
