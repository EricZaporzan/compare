# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView
from django.core.exceptions import PermissionDenied

from braces.views import LoginRequiredMixin

from .models import Comparison, ComparisonItem
from .forms import ComparisonCreateForm, ComparisonUpdateForm
from compare.users.models import User


class ComparisonCreateView(LoginRequiredMixin, CreateView):
    template_name = "comparisons/comparison_form.html"
    fields = ['title', 'description', 'date_starting', 'date_ending',]
    model = Comparison

    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        return super(ComparisonCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ComparisonCreateView, self).get_context_data(**kwargs)
        context['comparison_create_form'] = ComparisonCreateForm()
        return context


class ComparisonUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "comparisons/comparison_update.html"
    fields = ['title', 'description', 'date_starting', 'date_ending',]
    model = Comparison

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != self.get_object().owner.username:
            raise PermissionDenied # HTTP 403
        return super(ComparisonUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ComparisonUpdateView, self).get_context_data(**kwargs)
        instance = self.get_object()
        initial = {'title': instance.title,
                'description': instance.description,
                'date_starting': instance.date_starting.strftime("%m/%d/%Y"),
                'date_ending': instance.date_ending.strftime("%m/%d/%Y")}
        comparison_update_form = ComparisonUpdateForm(initial=initial)
        comparison_update_form.helper.form_action = reverse("comparisons:update", kwargs={'pk': instance.pk})
        context['comparison_update_form'] = comparison_update_form
        return context


class ComparisonDetailView(LoginRequiredMixin, DetailView):
    template_name = "comparisons/comparison_detail.html"
    model = Comparison
    slug_field = "pk"
    slug_url_kwarg = "pk"

    # Overriding the method to return related comparisonitems sorted by score
    def get_context_data(self, **kwargs):
        context = super(ComparisonDetailView, self).get_context_data(**kwargs)
        context['related_comparisonitems'] = ComparisonItem.objects.filter(comparison__exact = self.get_object()).order_by('-score')
        return context


class ComparisonListView(ListView):
    template_name = "comparisons/comparison_list.html"
    model = Comparison

    def get_queryset(self):
        username = self.request.GET.get('username')
        if username == None:
            return super(ComparisonListView, self).get_queryset()
        self.user = get_object_or_404(User, username=username)
        return Comparison.objects.filter(owner=self.user)

    def get_context_data(self, **kwargs):
        context = super(ComparisonListView, self).get_context_data(**kwargs)
        username = self.request.GET.get('username')
        if username == None:
            context['title'] = "All Comparisons"
        else:
            context['title'] = username + "'s Comparisons"
        return context

class ComparisonItemCreateView(LoginRequiredMixin, CreateView):
    template_name = "comparisons/comparison_submit.html"
    model = ComparisonItem
    fields = ['title', 'description', 'image',]

    def get_success_url(self):
        success_url =  reverse_lazy("comparisons:detail", kwargs={'pk': self.kwargs['pk']})
        return success_url

    def get_context_data(self, **kwargs):
        context = super(ComparisonItemCreateView, self).get_context_data(**kwargs)
        pk = self.kwargs['pk'] # Comparison will be the PK!
        context['comparison'] = get_object_or_404(Comparison, pk=pk)
        return context

    def form_valid(self, form):
        owner = self.request.user
        pk = self.kwargs['pk']
        comparison = get_object_or_404(Comparison, pk=pk)

        form.instance.owner = owner
        form.instance.comparison = comparison
        return super(ComparisonItemCreateView, self).form_valid(form)
