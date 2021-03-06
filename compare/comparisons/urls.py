# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='comparisons/home.html'), name="home"),
    url(
        regex=r'^compare/(?P<pk>[\d]+)/$',
        view=views.ComparisonPlatformView.as_view(),
        name='platform'
    ),
    url(
        regex=r'^browse/$',
        view=views.ComparisonListView.as_view(),
        name='browse'
    ),
    url(
        regex=r'^create/$',
        view=views.ComparisonCreateView.as_view(),
        name='create'
    ),
    url(
        regex=r'^(?P<pk>[\d]+)/$',
        view=views.ComparisonDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^(?P<pk>[\d]+)/update/$',
        view=views.ComparisonUpdateView.as_view(),
        name='update'
    ),
    url(
        regex=r'^submit/(?P<pk>[\d]+)/$',
        view=views.ComparisonItemCreateView.as_view(),
        name='submit'
    ),
]
