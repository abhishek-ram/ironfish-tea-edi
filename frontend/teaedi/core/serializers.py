from rest_framework import serializers
from .models import ShippingInvoice, ShippingInvoiceLine


class ShippingInvoiceLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingInvoiceLine
        exclude = ('id', 'shipping_invoice')


class ShippingInvoiceSerializer(serializers.ModelSerializer):
    isd_name = serializers.CharField(source='purchase_order.isd_name')
    isd_code = serializers.CharField(source='purchase_order.isd_code')
    lines = ShippingInvoiceLineSerializer(many=True)

    class Meta:
        model = ShippingInvoice
        fields = '__all__'
