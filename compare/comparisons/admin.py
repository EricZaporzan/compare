from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from .models import Comparison, ComparisonItem, ComparisonItemVote

class ComparisonAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "active",)
    readonly_fields = ("show_url",)

    def show_url(self, instance):
        url = reverse("comparisons:detail",
                    kwargs={"pk": instance.pk})
        response = format_html("""<a href="{0}">{1}</a>""", url, url)
        return response

    show_url.short_description = "Comparison URL"

class ComparisonItemAdmin(admin.ModelAdmin):
    list_display = ("comparison", "owner", "title", "score",)

class ComparisonItemVoteAdmin(admin.ModelAdmin):
    list_display = ("winner_initial_score", "loser_initial_score", "score_change")

admin.site.register(Comparison, ComparisonAdmin)
admin.site.register(ComparisonItem, ComparisonItemAdmin)
admin.site.register(ComparisonItemVote, ComparisonItemVoteAdmin)
