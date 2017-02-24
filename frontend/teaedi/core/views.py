from __future__ import unicode_literals
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import PurchaseOrder, ShippingInvoice
from .models import School, SalesPerson, Watcher
from .forms import WatcherForm, ActionForm
from .utils import GPWebService
import logging

# Get an instance of a logger
logger = logging.getLogger('teaedi')


class Index(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['counts'] = {
            'new_pos': PurchaseOrder.objects.filter(order_status='O').count(),
            'all_pos': PurchaseOrder.objects.all().count(),
            'new_si': ShippingInvoice.objects.exclude(
                invoice_status='A').count(),
            'all_si': ShippingInvoice.objects.all().count(),
        }
        context['purchase_orders'] = PurchaseOrder.objects.order_by(
            '-order_date')[:5]
        context['shipping_invoices'] = ShippingInvoice.objects.order_by(
            '-invoice_date')[:5]
        context['watchers'] = Watcher.objects.all()
        return context


class PurchaseOrderList(ListView):
    model = PurchaseOrder


class PurchaseOrderDetail(DetailView):
    model = PurchaseOrder


class PurchaseOrderReprocess(DetailView):
    model = PurchaseOrder

    def post(self, request, pk):
        po = self.get_object()
        po.order_status = 'O'
        po.save()
        messages.success(
            request, 'Purchase Order {} has been re-opened and can now be '
                     'imported in GP.'.format(pk))
        return HttpResponseRedirect(
            reverse_lazy('po-detail', args=[pk]))


class ShippingInvoiceList(FormView):
    template_name = 'core/shippinginvoice_list.html'
    form_class = ActionForm

    def get_context_data(self, **kwargs):
        context = super(
            ShippingInvoiceList, self).get_context_data(**kwargs)
        context['si_list'] = ShippingInvoice.objects.all()
        return context

    def form_valid(self, form):
        if not form.cleaned_data['id_list']:
            messages.error(
                self.request, 'At least one invoice must be selected for '
                              'action to be performed.')
        elif form.cleaned_data['action'] == 'process_selected':
            count_invoices = len(form.cleaned_data['id_list'])
            ShippingInvoice.objects.filter(
                pk__in=form.cleaned_data['id_list']).update(invoice_status='RP')
            messages.success(
                self.request, '{} Invoices have been marked for processing. '
                              'An email will be sent once invoice is '
                              'sent to TEA.'.format(count_invoices))
        return HttpResponseRedirect(reverse_lazy('shipping-invoice-list'))


class ShippingInvoiceDetail(DetailView):
    model = ShippingInvoice


class ShippingInvoiceRefresh(DetailView):
    model = ShippingInvoice

    def get(self, request, pk, **kwargs):
        shipping_invoice = self.get_object()
        try:
            gp_ws = GPWebService()
            gp_shipping_invoice = gp_ws.get_invoice_detail(pk)

            shipping_invoice.invoice_date = gp_shipping_invoice[
                'UserDefined']['Date01']
            shipping_invoice.actual_ship_date = gp_shipping_invoice[
                'UserDefined']['Date01']
            shipping_invoice.boxes = gp_shipping_invoice[
                                         'UserDefined']['List01'] or 0
            shipping_invoice.weight = gp_shipping_invoice[
                                          'UserDefined']['Text01'] or 0
            shipping_invoice.shipping_cost = gp_shipping_invoice[
                                                 'UserDefined']['List02'] or 0
            shipping_invoice.tracking_number = gp_shipping_invoice[
                                                   'UserDefined']['Text05'] or 0
            shipping_invoice.total_amount = gp_shipping_invoice[
                'TotalAmount']['Value']
            shipping_invoice.save()
            messages.success(
                request, 'Shipping Invoice {} has been successfully '
                         'refreshed.'.format(pk))
        except Exception, e:
            messages.error(request,  'Shipping Invoice {} could not be '
                                     'refreshed. Cause is: {}'.format(pk, e))
        finally:
            return HttpResponseRedirect(
                reverse_lazy('shipping-invoice-detail', args=[pk]))

# class ShippingInvoiceDelete(DeleteView):
#     model = ShippingInvoice
#     success_url = reverse_lazy('shipping-invoice-list')
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         messages.success(
#             request, 'Invoice "{0.invoice_id}" for order {0.purchase_order.pk}'
#                      ' has been deleted successfully'.format(self.object)
#         )
#         self.object.delete()
#         return HttpResponseRedirect(self.get_success_url())


class SchoolList(ListView):
    model = School


class SchoolCreate(SuccessMessageMixin, CreateView):
    model = School
    fields = ['isd_name', 'isd_code', 'district_enrollment', 'order',
              'region', 'sales_id', 'rsm', 'address_line1', 'address_line2',
              'address_line3', 'city', 'state', 'zip', 'contact_name',
              'contact_phone', 'contact_fax', 'contact_email', 'notes',
              'active', 'ag', 'fcs', 'ti', 'bm', 'careers', 'dag', 'dfcs',
              'dti', 'dbm', 'dcareers', 'careerdemo']
    success_url = reverse_lazy('school-list')
    success_message = 'School "%(isd_name)s" has been created successfully'


class SchoolUpdate(SuccessMessageMixin, UpdateView):
    model = School
    fields = ['isd_name', 'isd_code', 'district_enrollment', 'order',
              'region', 'sales_id', 'rsm', 'address_line1', 'address_line2',
              'address_line3', 'city', 'state', 'zip', 'contact_name',
              'contact_phone', 'contact_fax', 'contact_email', 'notes',
              'active', 'ag', 'fcs', 'ti', 'bm', 'careers', 'dag', 'dfcs',
              'dti', 'dbm', 'dcareers', 'careerdemo']
    success_url = reverse_lazy('school-list')
    success_message = 'School "%(isd_name)s" has been updated successfully'


class SalespersonList(ListView):
    model = SalesPerson


class SalespersonCreate(SuccessMessageMixin, CreateView):
    model = SalesPerson
    fields = ['name', 'school']
    success_url = reverse_lazy('salesperson-list')
    success_message = 'Salesperson "%(name)s" has been mapped to ' \
                      'school "%(school)s" successfully'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SalespersonCreate, self).get_context_data(**kwargs)
        valid_schools = []
        for school in School.objects.all():
            if not SalesPerson.objects.filter(school=school).exists():
                valid_schools.append((school.pk, school.isd_name))
        context['form'].fields['school'].choices = valid_schools
        return context


class SalespersonUpdate(SuccessMessageMixin, UpdateView):
    model = SalesPerson
    fields = ['name', 'school']
    success_url = reverse_lazy('salesperson-list')
    success_message = 'Salesperson "%(name)s" has been mapped to ' \
                      'school "%(school)s" successfully'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SalespersonUpdate, self).get_context_data(**kwargs)
        valid_schools = [(self.object.school.pk, self.object.school.isd_name)]
        for school in School.objects.all():
            if not SalesPerson.objects.filter(school=school).exists():
                valid_schools.append((school.pk, school.isd_name))
        context['form'].fields['school'].choices = valid_schools
        return context


class SalespersonDelete(DeleteView):
    model = SalesPerson
    success_url = reverse_lazy('salesperson-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(
            request, 'Mapping deleted between Salesperson "{0.name}" and '
                     'school "{0.school}" successfully'.format(self.object)
        )
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class WatcherList(ListView):
    model = Watcher


class WatcherCreate(SuccessMessageMixin, CreateView):
    model = Watcher
    form_class = WatcherForm
    success_url = reverse_lazy('watcher-list')
    success_message = 'Watcher "%(email_id)s" has been created successfully'


class WatcherUpdate(SuccessMessageMixin, UpdateView):
    model = Watcher
    form_class = WatcherForm
    success_url = reverse_lazy('watcher-list')
    success_message = 'Watcher "%(email_id)s" has been updated successfully'

