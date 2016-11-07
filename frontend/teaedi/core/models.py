from __future__ import unicode_literals
from django.db import models


class School(models.Model):
    isd_name = models.CharField(max_length=100)
    isd_code = models.CharField(max_length=30)
    district_enrollment = models.CharField(
        max_length=30, null=True, blank=True)
    order = models.CharField(max_length=30, null=True, blank=True)
    region = models.CharField(max_length=30, null=True, blank=True)
    sales_id = models.CharField(max_length=10)
    rsm = models.CharField(max_length=30, null=True, blank=True)
    address_line1 = models.TextField(max_length=100)
    address_line2 = models.TextField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    contact_name = models.CharField(max_length=30, null=True, blank=True)
    contact_phone = models.CharField(max_length=30, null=True, blank=True)
    contact_fax = models.CharField(max_length=30, null=True, blank=True)
    contact_email = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.isd_name

    class Meta:
        ordering = ['isd_name']


class Salesperson(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)


class PurchaseOrder(models.Model):
    ORDER_STATUSES = (
        ('O', 'Open'),
        ('P', 'Processed'),
        ('C', 'Cancelled'),
        ('M', 'Modified'),
    )

    order_id = models.CharField(max_length=30, primary_key=True)
    order_status = models.CharField(
        max_length=2, choices=ORDER_STATUSES, default='O')
    # batch_id = models.CharField(max_length=30)
    order_date = models.DateField()
    ship_date = models.DateField()
    customer_po = models.CharField(max_length=30)
    contract = models.CharField(max_length=30)
    isd_name = models.CharField(max_length=100)
    isd_code = models.CharField(max_length=30)
    sales_id = models.CharField(max_length=30, null=True)
    salesperson = models.CharField(max_length=30, null=True)
    address_line1 = models.TextField(max_length=100)
    address_line2 = models.TextField(max_length=100, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    contact_name = models.CharField(max_length=30)
    contact_phone = models.CharField(max_length=30, null=True)
    contact_fax = models.CharField(max_length=30, null=True)
    contact_email = models.CharField(max_length=100, null=True)
    owed_by_isd = models.DecimalField(
        max_digits=20, decimal_places=2, null=True)
    extra = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return self.order_id


class PurchaseOrderLine(models.Model):
    QUANTITY_UOM_CHOICES = (
        ('BK', 'Book'),
        ('KT', 'Kit'),
        ('SP', 'Software Product'),
        ('EA', 'EACH')
    )
    PRICE_CODE_CHOICES = (
        ('03', 'Contract'),
        ('04', 'No Charge'),
    )
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name='lines')
    sequence = models.CharField(max_length=30)
    quantity = models.IntegerField()
    quantity_uom = models.CharField(
        max_length=2, choices=QUANTITY_UOM_CHOICES)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    unit_price_code = models.CharField(
        max_length=2, choices=PRICE_CODE_CHOICES)
    sub_total = models.DecimalField(max_digits=20, decimal_places=2)
    ship_date = models.DateField(null=True)
    isbn = models.CharField(max_length=30)
    student_edition = models.CharField(max_length=30)
    student_edition_cost = models.CharField(max_length=30)
    school_district_owes = models.CharField(max_length=30)

    # The below fields are needed for handling PO Changes.
    original_quantity = models.IntegerField(null=True)
    cancelled = models.BooleanField(default=False)
    modified = models.BooleanField(default=False)
    added = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.purchase_order, self.sequence)


class ShippingInvoice(models.Model):
    INVOICE_STATUSES = (
        ('I', 'Imported'),
        ('P', 'Processed'),
        ('A', 'Accepted'),
        ('E', 'Accepted with Error'),
        ('R', 'Rejected'),
    )

    invoice_id = models.CharField(max_length=30, primary_key=True)
    invoice_status = models.CharField(
        max_length=2, choices=INVOICE_STATUSES, default='I')
    invoice_date = models.DateField()
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE,
        related_name='shipping_invoice'
    )
    actual_ship_date = models.DateField()
    boxes = models.IntegerField()
    weight = models.IntegerField()
    shipping_cost = models.DecimalField(max_digits=20, decimal_places=2)
    tracking_number = models.CharField(max_length=100)
    invoice_amount = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.invoice_id

    @property
    def invoice_total(self):
        return self.invoice_amount + self.shipping_cost


class ShippingInvoiceLine(models.Model):
    QUANTITY_UOM_CHOICES = (
        ('BK', 'Book'),
        ('KT', 'Kit'),
        ('SP', 'Software Product'),
        # ('EA', 'EACH')
    )

    shipping_invoice = models.ForeignKey(
        ShippingInvoice, on_delete=models.CASCADE, related_name='lines')
    sequence = models.CharField(max_length=30)
    quantity = models.IntegerField()
    quantity_uom = models.CharField(
        max_length=2, choices=QUANTITY_UOM_CHOICES)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    # sub_total = models.DecimalField(max_digits=20, decimal_places=2)
    actual_ship_date = models.DateField(null=True)
    isbn = models.CharField(max_length=30)
    student_edition = models.CharField(max_length=30)
    student_edition_cost = models.CharField(max_length=30)
    school_district_owes = models.CharField(max_length=30, null=True)

    @property
    def sub_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return '{} {}'.format(self.shipping_invoice, self.sequence)


class Watcher(models.Model):
    EVENT_CHOICES = (
        ('PO_NEW', 'New Purchase Order Imported'),
        ('PO_UPD', 'Purchase Order Updated/Cancelled'),
        # ('SI_PRO', 'Shipping and Invoice Document Processed'),
        ('SI_ACK', 'Shipping and Invoice Document Acknowledged')
    )

    email_id = models.EmailField(unique=True)
    events = models.CharField(max_length=200)

    def get_events_display(self):
        events_display = []
        event_choices_dict = {k: v for k, v in self.EVENT_CHOICES}
        for event in eval(self.events):
            events_display.append(event_choices_dict[event])
        return events_display
