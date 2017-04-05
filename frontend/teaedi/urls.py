from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from .core import views, apis
urlpatterns = [
    # URLs for the django admin site
    url(r'^admin', admin.site.urls),

    # URLs for the TEAEDI app
    url(r'^index/$', login_required(views.Index.as_view()), name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/index/'}, name='logout'),
    url(r'^purchase_order/$',
        login_required(views.PurchaseOrderList.as_view()),
        name='po-list'),
    url(r'^purchase_order/(?P<pk>[a-zA-Z0-9]+)/$',
        login_required(views.PurchaseOrderDetail.as_view()),
        name='po-detail'),
    url(r'^purchase_order/(?P<pk>[a-zA-Z0-9]+)/reprocess/$',
        login_required(views.PurchaseOrderReprocess.as_view()),
        name='po-reprocess'),

    url(r'^shipping_invoice/pending/$',
        login_required(views.ShippingInvoicePending.as_view()),
        name='shipping-invoice-pending'),
    url(r'^shipping_invoice/all/$',
        login_required(views.ShippingInvoiceAll.as_view()),
        name='shipping-invoice-all'),
    url(r'^shipping_invoice/(?P<pk>[a-zA-Z0-9]+)/$',
        login_required(views.ShippingInvoiceDetail.as_view()),
        name='shipping-invoice-detail'),
    url(r'^shipping_invoice/(?P<pk>[a-zA-Z0-9]+)/refresh/$',
        login_required(views.ShippingInvoiceRefresh.as_view()),
        name='shipping-invoice-refresh'),

    url(r'watcher/$',
        login_required(views.WatcherList.as_view()),
        name='watcher-list'),
    url(r'watcher/add/$',
        login_required(views.WatcherCreate.as_view()),
        name='watcher-add'),
    url(r'watcher/(?P<pk>[0-9]+)/$',
        login_required(views.WatcherUpdate.as_view()),
        name='watcher-update'),

    url(r'new-po-list/$',
        login_required(views.NewPOList.as_view()),
        name='new-po-list'),
    url(r'all-po-list/$',
        login_required(views.AllPOList.as_view()),
        name='all-po-list'),
    url(r'pending-si-list/$',
        login_required(views.PendingSIList.as_view()),
        name='pending-si-list'),
    url(r'all-si-list/$',
        login_required(views.AllSIList.as_view()),
        name='all-si-list'),

    # URLs for the TEAEDI REST API
    url(r'^api/purchase_order/$', apis.CRUDPurchaseOrder.as_view()),
    url(r'^api/process_acknowledgment/$', apis.ProcessAcknowledgment.as_view()),
    url(r'^api/shipping_invoice/$', apis.ShippingInvoiceList.as_view()),
    url(r'^api/shipping_invoice/(?P<pk>[0-9]+)/processed/$',
        apis.ShippingInvoiceMarkProcessed.as_view()),

    url(r'^.*', login_required(views.Index.as_view())),
]

