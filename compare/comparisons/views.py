# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView
from django.core.exceptions import PermissionDenied

from braces.views import LoginRequiredMixin

from .models import Comparison, ComparisonItem
from .forms import ComparisonCreateForm, ComparisonUpdateForm, ComparisonItemCreateForm
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

    # Users should only be able to update their own comparisons. Handled here.
    def dispatch(self, request, *args, **kwargs):
        if request.user.username != self.get_object().owner.username:
            messages.error(request, "This doesn't belong to you, so you can't edit it!")
            return redirect(reverse('comparisons:detail', kwargs={'pk': self.kwargs['pk']}))
        return super(ComparisonUpdateView, self).dispatch(request, *args, **kwargs)

    # Handles the prepopulation of the form (since there's already stuff there)
    def get_context_data(self, **kwargs):
        context = super(ComparisonUpdateView, self).get_context_data(**kwargs)
        instance = self.get_object()

        # This is ugly; let's change the model at some point to make this required or default to something.
        if instance.date_ending:
            date_ending = instance.date_ending.strftime("%m/%d/%Y")
        else:
            date_ending = None

        initial = {'title': instance.title,
                'description': instance.description,
                'date_starting': instance.date_starting.strftime("%m/%d/%Y"),
                'date_ending': date_ending}
        comparison_update_form = ComparisonUpdateForm(initial=initial)
        comparison_update_form.helper.form_action = reverse("comparisons:update", kwargs={'pk': instance.pk})
        context['comparison_update_form'] = comparison_update_form
        return context

    def form_valid(self, form):
        if form.instance.owner.username != request.user.username:
            messages.error("This doesn't belong to you, so you can't edit it!")
            return redirect(reverse('comparisons:detail', kwargs={'pk': self.kwargs['pk']}))
        return super(ComparisonUpdateView, self).form_valid(form)


class ComparisonDetailView(LoginRequiredMixin, DetailView):
    template_name = "comparisons/comparison_detail.html"
    model = Comparison
    slug_field = "pk"
    slug_url_kwarg = "pk"

    # Overriding the method to return related comparisonitems sorted by score
    def get_context_data(self, **kwargs):
        context = super(ComparisonDetailView, self).get_context_data(**kwargs)
        context['current_day'] = date.today()
        context['related_comparisonitems'] = ComparisonItem.objects.filter(comparison__exact = self.get_object()).order_by('-score')
        return context


# This view returns the full list of comparisons if there's no ?username token.
# If there is a ?username token it'll return all of that user's comparisons.
class ComparisonListView(ListView):
    template_name = "comparisons/comparison_list.html"
    model = Comparison

    # This handles the filtering on the username
    def get_queryset(self):
        username = self.request.GET.get('username')
        if username == None:
            return super(ComparisonListView, self).get_queryset()
        self.user = get_object_or_404(User, username=username)
        return Comparison.objects.filter(owner=self.user)

    # Passes down different context depending on the token existence.
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

    # Rather not let a user submit to a contest if it's already over. Raise a 403 instead.
    def dispatch(self, request, *args, **kwargs):
        comparison = get_object_or_404(Comparison, pk=self.kwargs['pk'])
        today = date.today()
        if (comparison.date_starting and today < comparison.date_starting) or (comparison.date_ending and today > comparison.date_ending):
            messages.error(request, "Sorry, you can't submit to a competition that's already ended!")
            return redirect(reverse('comparisons:detail', kwargs={'pk': self.kwargs['pk']}))
        return super(ComparisonItemCreateView, self).dispatch(request, *args, **kwargs)

    # After a successful submit, returns the user to that comparison's page
    def get_success_url(self):
        success_url =  reverse_lazy("comparisons:detail", kwargs={'pk': self.kwargs['pk']})
        return success_url

    def get_context_data(self, **kwargs):
        context = super(ComparisonItemCreateView, self).get_context_data(**kwargs)
        comparison_item_create_form = ComparisonItemCreateForm()
        comparison_item_create_form.helper.form_action = reverse("comparisons:submit", kwargs={'pk': self.kwargs['pk']})
        pk = self.kwargs['pk'] # pk of the parent comparison!
        context['comparison'] = get_object_or_404(Comparison, pk=pk)
        context['comparison_item_create_form'] = comparison_item_create_form
        return context

    def form_valid(self, form):
        owner = self.request.user
        pk = self.kwargs['pk']
        comparison = get_object_or_404(Comparison, pk=pk)
        form.instance.owner = owner
        form.instance.comparison = comparison
        messages.success(self.request, "Your submission has been accepted!")
        return super(ComparisonItemCreateView, self).form_valid(form)
