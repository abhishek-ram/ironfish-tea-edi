from __future__ import unicode_literals
from django.views.generic import ListView, DetailView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .models import PurchaseOrder, ShippingInvoice
from .models import ShippingInvoiceLine, PurchaseOrderLine
from .models import School, Salesperson, Watcher
from .forms import WatcherForm, ShippingInvoiceForm
from traceback import format_exc
import logging

# Get an instance of a logger
logger = logging.getLogger('teaedi')


def index(request):
    return render(request, 'core/index.html')


class PurchaseOrderList(ListView):
    model = PurchaseOrder


class PurchaseOrderDetail(DetailView):
    model = PurchaseOrder


class ShippingInvoiceCreate(FormView):
    template_name = 'core/shippinginvoice_form.html'
    form_class = ShippingInvoiceForm

    def form_valid(self, form):
        """Create the shipping invoice object and related line items"""
        header_data = form.cleaned_data['header_file']
        detail_data = form.cleaned_data['detail_file']

        # Check if the invoice already exists in the DB
        if ShippingInvoice.objects.filter(pk=header_data[12]).exists():
            messages.error(
                self.request, 'Invoice with this ID already '
                              'exists in the database.')
            return HttpResponseRedirect(reverse_lazy('shipping-invoice-add'))

        # Fetch the PO related to this invoice from the DB
        original_po = PurchaseOrder.objects.filter(pk=header_data[0]).first()
        if not original_po:
            messages.error(
                self.request, 'Failed to create shipping Invoice. '
                              'Original PO not found in the database')
            return HttpResponseRedirect(reverse_lazy('shipping-invoice-add'))

        try:
            # Create the shipping invoice object.
            si = ShippingInvoice.objects.create(
                purchase_order=original_po,
                invoice_id=header_data[12],
                invoice_date=header_data[10],
                actual_ship_date=header_data[1],
                boxes=header_data[2],
                weight=header_data[3],
                shipping_cost=header_data[4],
                tracking_number=header_data[5],
                invoice_amount=header_data[8]
            )
            
            for line in detail_data:
                po_line = PurchaseOrderLine.objects.get(
                    purchase_order=original_po, isbn=line[3])
                # Create the shipping invoice line object.
                ShippingInvoiceLine.objects.create(
                    shipping_invoice=si,
                    sequence=po_line.sequence,
                    quantity=line[1],
                    quantity_uom=line[4],
                    unit_price=line[2],
                    isbn=line[3],
                    actual_ship_date=line[5],
                    student_edition=po_line.student_edition,
                    student_edition_cost=po_line.student_edition_cost,
                    school_district_owes=po_line.student_edition_cost,
                )
        except Exception:
            logger.error('Failed to process invoice {}, Detailed '
                         'error is \n {}'.format(header_data[12],
                                                 format_exc()))
            messages.error(
                self.request, 'Failed to create shipping Invoice. '
                              'Unknown processing error, contact site admin.')
            return HttpResponseRedirect(reverse_lazy('shipping-invoice-add'))
        else:
            messages.success(
                self.request, 'Shipping Invoice {} created '
                              'successfully.'.format(si.invoice_id))
            return HttpResponseRedirect(
                reverse_lazy('shipping-invoice-detail', args=[si.invoice_id]))


class ShippingInvoiceList(ListView):
    model = ShippingInvoice


class ShippingInvoiceDetail(DetailView):
    model = ShippingInvoice

    def post(self, request):
        self.object = self.get_object()


class ShippingInvoiceDelete(DeleteView):
    model = ShippingInvoice
    success_url = reverse_lazy('shipping-invoice-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(
            request, 'Invoice "{0.invoice_id}" for order {0.purchase_order.pk}'
                     ' has been deleted successfully'.format(self.object)
        )
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class SchoolList(ListView):
    model = School


class SalespersonList(ListView):
    model = Salesperson


class SalespersonCreate(SuccessMessageMixin, CreateView):
    model = Salesperson
    fields = ['name', 'school']
    success_url = reverse_lazy('salesperson-list')
    success_message = 'Salesperson "%(name)s" has been mapped to ' \
                      'school "%(school)s" successfully'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SalespersonCreate, self).get_context_data(**kwargs)
        valid_schools = []
        for school in School.objects.all():
            if not Salesperson.objects.filter(school=school).exists():
                valid_schools.append((school.pk, school.isd_name))
        context['form'].fields['school'].choices = valid_schools
        return context


class SalespersonUpdate(SuccessMessageMixin, UpdateView):
    model = Salesperson
    fields = ['name', 'school']
    success_url = reverse_lazy('salesperson-list')
    success_message = 'Salesperson "%(name)s" has been mapped to ' \
                      'school "%(school)s" successfully'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SalespersonUpdate, self).get_context_data(**kwargs)
        valid_schools = [(self.object.school.pk, self.object.school.isd_name)]
        for school in School.objects.all():
            if not Salesperson.objects.filter(school=school).exists():
                valid_schools.append((school.pk, school.isd_name))
        context['form'].fields['school'].choices = valid_schools
        return context


class SalespersonDelete(DeleteView):
    model = Salesperson
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

