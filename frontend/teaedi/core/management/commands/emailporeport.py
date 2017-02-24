from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from ....core.models import PurchaseOrder, Watcher
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger('teaedi')


class Command(BaseCommand):
    help = 'Email a report of all POs received in the past 24 hours'

    def handle(self, *args, **options):
        # Notify any watchers that are listening for SI Processed
        watchers = [w.email_id for w in
                    Watcher.objects.filter(events__contains='PO_RPT')]
        if watchers:
            yesterday = timezone.localtime(timezone.now()) - timedelta(days=1)
            logger.info('Emailing daily order report to :{}'.format(watchers))
            email_body = render_to_string(
                'emails/purchaseorder_report.html',
                {'po_list': PurchaseOrder.objects.filter(order_date__gte=yesterday)}
            )
            send_mail('[TEAEDI] Daily Purchase Order Report',
                      from_email='',
                      recipient_list=watchers,
                      message='',
                      html_message=email_body)
