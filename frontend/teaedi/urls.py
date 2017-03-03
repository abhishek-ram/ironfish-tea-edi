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

    url(r'school/$',
        login_required(views.SchoolList.as_view()),
        name='school-list'),
    url(r'school/add/$',
        login_required(views.SchoolCreate.as_view()),
        name='school-add'),
    url(r'school/(?P<pk>[0-9]+)/$',
        views.SchoolUpdate.as_view(),
        name='school-update'),

    url(r'salesperson/$',
        login_required(views.SalespersonList.as_view()),
        name='salesperson-list'),
    url(r'salesperson/add/$',
        login_required(views.SalespersonCreate.as_view()),
        name='salesperson-add'),
    url(r'salesperson/(?P<pk>[0-9]+)/$',
        login_required(views.SalespersonUpdate.as_view()),
        name='salesperson-update'),
    url(r'salesperson/(?P<pk>[0-9]+)/delete/$',
        login_required(views.SalespersonDelete.as_view()),
        name='salesperson-delete'),

    url(r'watcher/$',
        login_required(views.WatcherList.as_view()),
        name='watcher-list'),
    url(r'watcher/add/$',
        login_required(views.WatcherCreate.as_view()),
        name='watcher-add'),
    url(r'watcher/(?P<pk>[0-9]+)/$',
        login_required(views.WatcherUpdate.as_view()),
        name='watcher-update'),

    # URLs for the TEAEDI REST API
    url(r'^api/purchase_order/$', apis.CRUDPurchaseOrder.as_view()),
    url(r'^api/process_acknowledgment/$', apis.ProcessAcknowledgment.as_view()),
    url(r'^api/shipping_invoice/$', apis.ShippingInvoiceList.as_view()),
    url(r'^api/shipping_invoice/(?P<pk>[0-9]+)/processed/$',
        apis.ShippingInvoiceMarkProcessed.as_view()),

    url(r'^.*', login_required(views.Index.as_view())),
] 
