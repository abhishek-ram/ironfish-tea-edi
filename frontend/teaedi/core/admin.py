from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderLine, ShippingInvoice


class PurchaseOrderAdmin(admin.ModelAdmin):
    pass


class PurchaseOrderLineAdmin(admin.ModelAdmin):
    pass


class ShippingInvoiceAdmin(admin.ModelAdmin):
    pass


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderLine, PurchaseOrderLineAdmin)
admin.site.register(ShippingInvoice, ShippingInvoiceAdmin)
