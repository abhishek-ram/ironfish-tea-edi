from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderLine


class PurchaseOrderAdmin(admin.ModelAdmin):
    pass


class PurchaseOrderLineAdmin(admin.ModelAdmin):
    pass

admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderLine, PurchaseOrderLineAdmin)

