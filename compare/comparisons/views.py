# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView

from braces.views import LoginRequiredMixin

from .models import Comparison, ComparisonItem

class ComparisonCreateView(LoginRequiredMixin, CreateView):
    fields = ['title', 'description', 'date_starting', 'date_ending',]
    model = Comparison
    def form_valid(self, form):
        owner = self.request.user
        form.instance.owner = owner
        return super(ComparisonCreateView, self).form_valid(form)


class ComparisonUpdateView(LoginRequiredMixin, UpdateView):
    model = Comparison

class ComparisonDetailView(LoginRequiredMixin, DetailView):
    model = Comparison
    slug_field = "pk"
    slug_url_kwarg = "pk"

    # Overriding the method to return related comparisonitems sorted by score
    def get_context_data(self, **kwargs):
        context = super(ComparisonDetailView, self).get_context_data(**kwargs)
        context['related_comparisonitems'] = ComparisonItem.objects.filter(comparison__exact = self.get_object()).order_by('-score')
        return context

class ComparisonListView(ListView):
    model = Comparison
