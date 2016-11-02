from __future__ import unicode_literals
from django.db import models


class School(models.Model):
    isd_name = models.CharField(max_length=100)
    isd_code = models.CharField(max_length=30)
    district_enrollment = models.CharField(max_length=30)
    order = models.IntegerField()
    region = models.IntegerField()
    sales_id = models.CharField(max_length=10)
    rsm = models.CharField(max_length=30)
    address_line1 = models.TextField(max_length=100)
    address_line2 = models.TextField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    contact_name = models.CharField(max_length=30)
    contact_phone = models.CharField(max_length=30)
    contact_fax = models.CharField(max_length=30)
    contact_email = models.CharField(max_length=100)
    notes = models.TextField(max_length=100)


class Salesperson(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)


class PurchaseOrder(models.Model):
    ORDER_STATUSES = (
        ('O', 'Open'),
        ('P', 'Processed'),
        ('C', 'Cancelled'),
        ('S', 'Shipped and Invoiced'),
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
    address_line1 = models.TextField(max_length=100)
    address_line2 = models.TextField(max_length=100, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    contact_name = models.CharField(max_length=30)
    contact_phone = models.CharField(max_length=30)
    contact_fax = models.CharField(max_length=30)
    contact_email = models.CharField(max_length=100)
    owed_by_isd = models.DecimalField(
        max_digits=20, decimal_places=2, null=True)
    extra = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return self.order_id


class PurchaseOrderLine(models.Model):
    QUANTITY_UOM_CHOICES = (
        ('BK', 'Book'),
        ('KT', 'Kit'),
        ('SP', 'Software Product')
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
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    ship_date = models.DateField(null=True)
    isbn = models.CharField(max_length=30)
    student_edition = models.CharField(max_length=30)
    student_edition_cost = models.CharField(max_length=30)
    school_district_owes = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.purchase_order, self.sequence)
