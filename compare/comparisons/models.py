# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from datetime import datetime

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from sorl.thumbnail import ImageField
from elo import rate_1vs1

from compare.users.models import User

# Extra functions, can be used by any of these models
def upload_to(instance, filename):
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")[:-3] + "/" + filename


class Comparison(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(_("What should it be called?"), max_length=255)
    description = models.TextField(_("Outline the rules, guidelines, and anything else important about this comparison."), blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_starting = models.DateField(_("When should we start?"), blank=True, default=timezone.now)
    date_ending = models.DateField(_("When should we finish?"), blank=True, null=True)
    active = models.BooleanField(_("Is it happening right now?"), default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('comparisons:detail', kwargs={'pk': self.pk})


class ComparisonItem(models.Model):
    comparison = models.ForeignKey(Comparison)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(_("Name"), max_length=255, blank=True)
    description = models.TextField(_("Give a brief description of the submission"), blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=1400)
    image = ImageField(upload_to=upload_to)

    def __str__(self):
        if(self.title == ""):
            return str(self.owner.username) + "'s submission to the '" + str(self.comparison.title) + "' comparison"
        else:
            return self.title

    # def get_absolute_url(self): # will go here, but right now comparisonitems are mainly accessable through their parent comparisons.


class ComparisonItemVote(models.Model):
    winner = models.ForeignKey(ComparisonItem, related_name="winner")
    loser = models.ForeignKey(ComparisonItem, related_name="loser")
    # These are here because we might want to track the progression of scores
    winner_initial_score = models.IntegerField(default=1400)
    loser_initial_score = models.IntegerField(default=1400)
    # The winner will go up by score_change; the loser will go down by the same.
    score_change = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.winner_initial_score = self.winner.score
        self.loser_initial_score = self.loser.score

        winner_new_score, loser_new_score = rate_1vs1(self.winner_initial_score, self.loser_initial_score)
        winner_new_int_score = int(winner_new_score)
        loser_new_int_score = int(loser_new_score)

        self.score_change = winner_new_int_score - self.winner_initial_score
        super(ComparisonItemVote, self).save(*args, **kwargs)

        self.winner.score = winner_new_int_score
        self.winner.save()

        self.loser.score = loser_new_int_score
        self.loser.save()
