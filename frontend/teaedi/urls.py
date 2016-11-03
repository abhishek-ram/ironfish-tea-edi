from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required
from .core import views, apis

urlpatterns = [
    # URLs for the django admin site
    url(r'^admin/', admin.site.urls),

    # URLs for the TEAEDI app
    url(r'^index/', login_required(views.index), name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/index/'}, name='logout'),
    url(r'^purchase_orders/$',
        login_required(views.PurchaseOrderList.as_view()),
        name='po-list'),
    url(r'^purchase_orders/(?P<pk>[a-zA-Z0-9]+)/$',
        login_required(views.PurchaseOrderDetail.as_view()),
        name='po-detail'),
    url(r'school/$', views.SchoolList.as_view(), name='school-list'),
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

    # URLs for the TEAEDI REST API
    url(r'^api/purchase_order',
        apis.CreatePurchaseOrder.as_view(),
        name='po-create'),

    url(r'^.*', views.index),
] 
