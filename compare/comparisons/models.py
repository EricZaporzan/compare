# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from compare.users.models import User

class Comparison(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(_("What should it be called?"), max_length=255)
    description = models.TextField(_("Outline the rules, guidelines, and anything else important about this comparison."), blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_ending = models.DateTimeField(_("When should we finish?"), blank=True)
    active = models.BooleanField(_("Is it happening right now?"), default=True)

    def __str__(self):
        return self.title

class ComparisonItem(models.Model):
    comparison = models.ForeignKey(Comparison)
    owner = models.ForeignKey(User)
    title = models.CharField(_("Name"), max_length=255, blank=True)
    description = models.TextField(_("Give a brief description of the submission"), blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    image_url = models.URLField()
