from rest_framework import serializers
from .models import ShippingInvoice, ShippingInvoiceLine


class ShippingInvoiceLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingInvoiceLine
        exclude = ('id', 'shipping_invoice')


class ShippingInvoiceSerializer(serializers.ModelSerializer):
    isd_name = serializers.CharField(source='purchase_order.isd_name')
    isd_code = serializers.CharField(source='purchase_order.isd_code')
    contract = serializers.CharField(source='purchase_order.contract')
    purchase_order = serializers.CharField(source='purchase_order.customer_po')
    purchase_order_date = serializers.CharField(
        source='purchase_order.order_date')
    Lines = ShippingInvoiceLineSerializer(many=True, source='lines')

    class Meta:
        model = ShippingInvoice
        fields = '__all__'
