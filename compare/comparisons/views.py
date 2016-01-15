# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView
from django.core.exceptions import PermissionDenied

from braces.views import LoginRequiredMixin

from .models import Comparison, ComparisonItem
from .forms import ComparisonCreateForm, ComparisonUpdateForm
from compare.users.models import User


class ComparisonCreateView(LoginRequiredMixin, CreateView):
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
        data = {'title': instance.title, 'description': instance.description, 'date_starting': instance.date_starting, 'date_ending': instance.date_ending }
        comparison_update_form = ComparisonUpdateForm(initial=data)
        comparison_update_form.helper.form_action = reverse("comparisons:update", kwargs={'pk': instance.pk})

        context['comparison_update_form'] = comparison_update_form
        return context


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

    def get_queryset(self):
        username = self.request.GET.get('username')
        if username == None:
            return super(ComparisonListView, self).get_queryset()
        self.user = get_object_or_404(User, username=username)
        return Comparison.objects.filter(owner=self.user)
