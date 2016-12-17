from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderLine
from .models import ShippingInvoice, ShippingInvoiceLine


class PurchaseOrderAdmin(admin.ModelAdmin):
    pass


class PurchaseOrderLineAdmin(admin.ModelAdmin):
    pass


class ShippingInvoiceAdmin(admin.ModelAdmin):
    pass


class ShippingInvoiceLineAdmin(admin.ModelAdmin):
    pass


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderLine, PurchaseOrderLineAdmin)
admin.site.register(ShippingInvoice, ShippingInvoiceAdmin)
admin.site.register(ShippingInvoiceLine, ShippingInvoiceLineAdmin)
