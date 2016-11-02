from __future__ import unicode_literals
from django.db import models


class PurchaseOrder(models.Model):
    ORDER_STATUSES = (
        ('O', 'Open'),
        ('P', 'Processed'),
        ('C', 'Cancelled'),
        ('S', 'Shipped and Invoiced'),
    )

    order_id = models.CharField(max_length=30, primary_key=True)
    external_order_id = models.CharField(max_length=30)
    order_date = models.DateField()
    order_status = models.CharField(
        max_length=2, choices=ORDER_STATUSES, default='O')
    requisition_id = models.CharField(max_length=30)
    ship_earliest = models.DateField(null=True)
    ship_latest = models.DateField(null=True)
    ship_to_name = models.CharField(max_length=60)
    ship_to_id = models.CharField(max_length=30)

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
    line_number = models.CharField(max_length=30)
    quantity = models.IntegerField()
    quantity_uom = models.CharField(
        max_length=2, choices=QUANTITY_UOM_CHOICES)
    unit_price = models.DecimalField(max_digits=20, decimal_places=4)
    unit_price_code = models.CharField(
        max_length=2, choices=PRICE_CODE_CHOICES)
    isbn = models.CharField(max_length=30)
    student_edition = models.CharField(max_length=30)
    student_edition_cost = models.CharField(max_length=30)
    school_district_owes = models.CharField(max_length=30)

    def __str__(self):
        return '{} {}'.format(self.purchase_order, self.line_number)
