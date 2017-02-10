from __future__ import unicode_literals
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from .models import PurchaseOrder, ShippingInvoice
from .models import ShippingInvoiceLine, PurchaseOrderLine
from .models import School, SalesPerson, Watcher
from .forms import WatcherForm, ShippingInvoiceForm
from traceback import format_exc
import logging
import csv
import os
import time

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

            quantity_uom_codes = {
                v: k for k, v in ShippingInvoiceLine.QUANTITY_UOM_CHOICES}
            for line in detail_data:
                po_line = PurchaseOrderLine.objects.get(
                    purchase_order=original_po, isbn=line[3])
                # Create the shipping invoice line object.
                ShippingInvoiceLine.objects.create(
                    shipping_invoice=si,
                    sequence=po_line.sequence,
                    quantity=line[1],
                    quantity_uom=quantity_uom_codes[line[4]],
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

    def post(self, request, pk):
        si = self.get_object()
        output_filename = os.path.join(
            settings.TEAEDI['SHIPPING_INVOICE']['EXPORT_FOLDER'],
            'Invoice_{}_{}.csv'.format(pk, int(time.time())))
        with open(output_filename, 'wb') as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([
                'Header',
                '17528036696002',
                'TEXASEDUAGENCY',
                pk,
                si.invoice_date.strftime('%Y%m%d'),
                si.boxes,
                si.weight,
                si.shipping_cost,
                si.tracking_number,
                si.purchase_order.isd_name,
                si.purchase_order.isd_code,
                si.invoice_amount,
                si.purchase_order.pk,
                0,
                si.purchase_order.order_date.strftime('%Y%m%d'),
                si.purchase_order.contract
            ])

            for line in si.lines.all():
                csv_writer.writerow([
                    'LineItem',
                    line.sequence,
                    line.unit_price,
                    line.isbn,
                    line.student_edition,
                    line.student_edition_cost,
                    line.quantity,
                    line.quantity_uom,
                    line.actual_ship_date.strftime('%Y%m%d')
                ])

        si.invoice_status = 'P'
        si.save()
        messages.success(
            request, 'Shipping Invoice {} has been sent to TEA.'.format(pk))
        return HttpResponseRedirect(
            reverse_lazy('shipping-invoice-detail', args=[pk]))


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

