from __future__ import unicode_literals
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .models import PurchaseOrder
from .models import School, Salesperson


def index(request):
    return render(request, 'core/index.html')


class PurchaseOrderList(ListView):
    model = PurchaseOrder


class PurchaseOrderDetail(DetailView):
    model = PurchaseOrder

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PurchaseOrderDetail, self).get_context_data(**kwargs)
        context['school'] = School.objects.filter(
            isd_code=self.object.isd_code.lstrip('0')).first()
        context['salesperson'] = Salesperson.objects.filter(
            school=context['school']).first()
        return context


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
